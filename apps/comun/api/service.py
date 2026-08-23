import copy
import traceback
from typing import Any, Callable, Optional, Type

from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from django.db.models import ManyToManyField, Model
from django_filters import FilterSet
from ninja_extra import ModelService, service_resolver
from ninja_extra.context import RouteContext
from ninja_extra.exceptions import ValidationError

from apps.comun.management.commands.generators.consts import DISPLAY_NAME


class GenericModelService(ModelService):  # noqa
    def __init__(
        self,
        model,
        pre_save: Optional[Callable] = None,
        post_save: Optional[Callable] = None,
        filterset_class: Optional[Type[FilterSet]] = None,
    ):
        super().__init__(model)
        self.pre_save: Optional[Callable] = pre_save
        self.post_save: Optional[Callable] = post_save
        self.filterset_class: Optional[Type[FilterSet]] = filterset_class

    def _sync_display_name(self, instance):
        """Sincroniza el campo display_name con el campo principal del modelo.

        Similar a la lógica en AbstractMethods.save() pero adaptada para la API.
        """
        # Check if model has a 'display_name' field
        if not hasattr(instance, DISPLAY_NAME):
            return

        try:
            display_name_field = instance._meta.get_field(DISPLAY_NAME)
            field_key = getattr(display_name_field, DISPLAY_NAME, None)

            # Si no hay field_key configurado, no hay nada que sincronizar
            if not field_key:
                return

            # Obtener el valor del campo principal (ej: 'genre', 'nombre')
            principal_value = getattr(instance, field_key, None)

            # Si el campo principal tiene valor, copiarlo a display_name
            if principal_value:
                # Get the number of records with the same value or starting with it
                count_records = instance.__class__.objects.filter(
                    **{f"{field_key}__startswith": principal_value}
                ).count()

                # If updating an existing record, exclude itself from the count
                if instance.pk:
                    count_records = (
                        instance.__class__.objects.filter(**{f"{field_key}__startswith": principal_value})
                        .exclude(pk=instance.pk)
                        .count()
                    )

                # If no records exist with the same value, set the original, else create a unique one
                new_display_name = principal_value if count_records == 0 else f"{principal_value}_{count_records + 1}"
                setattr(instance, DISPLAY_NAME, new_display_name)

        except Exception:
            # Si hay algún error (campo no existe, etc), continuar sin sincronizar
            pass

    def _get_auto_fields(self, instance):
        """Retorna lista de campos que se asignan automáticamente y no deben validarse.

        Incluye: display_name, campos de auditoría (created_by, updated_by, etc)
        """
        exclude_fields = []

        # Siempre excluir display_name porque se genera automáticamente
        if hasattr(instance, DISPLAY_NAME):
            exclude_fields.append(DISPLAY_NAME)

        # Excluir campos de auditoría comunes
        audit_fields = ["created_by", "updated_by", "created_at", "updated_at", "deleted_at"]
        for field in audit_fields:
            if hasattr(instance, field):
                exclude_fields.append(field)

        return exclude_fields

    def _validate_instance(self, instance):
        """Valida la instancia del modelo usando full_clean de Django.

        Maneja y convierte errores de validación al formato de la API.
        """
        try:
            # Validar solo los campos que vinieron en el schema
            instance.full_clean(exclude=self._get_auto_fields(instance))
        except DjangoValidationError as e:
            self._handle_django_validation_error(e)

    def _handle_django_validation_error(self, e: DjangoValidationError):
        """Convierte DjangoValidationError a ValidationError de ninja_extra con el formato correcto para la API."""
        errors = []

        if hasattr(e, "error_dict"):
            # Errores por campo
            for field, field_errors in e.error_dict.items():
                for error in field_errors:
                    errors.append({"loc": ["body", field], "msg": str(error.message), "type": "value_error"})
        elif hasattr(e, "error_list"):
            # Errores generales (no de campo específico)
            for error in e.error_list:
                errors.append({"loc": ["body"], "msg": str(error.message), "type": "value_error"})
        else:
            # Fallback para errores simples
            errors.append({"loc": ["body"], "msg": str(e), "type": "value_error"})

        raise ValidationError(errors)

    def _separate_m2m_fields(self, data: dict) -> tuple[dict, dict]:
        # Separate m2m fields from regular fields
        result = copy.deepcopy(data)
        m2m_field_names = {field.name for field in self.model._meta.get_fields() if isinstance(field, ManyToManyField)}
        m2m_data = {}
        for field_name in list(result):
            if field_name in m2m_field_names:
                m2m_data[field_name] = result.pop(field_name)

        return m2m_data, result

    def _validate_m2m_options(self, instance: Model, field_name: str, values: list[int]):
        model_meta = instance._meta

        try:
            field = model_meta.get_field(field_name)
        except Exception:
            self._handle_django_validation_error(
                DjangoValidationError(f"'{field_name}' is not a valid field on {self.model.__name__}")
            )

        if not isinstance(field, ManyToManyField):
            self._handle_django_validation_error(DjangoValidationError(f"'{field_name}' is not a ManyToManyField"))

        if not values:
            return  # empty list is valid unless business rules say otherwise

        related_model = field.remote_field.model

        # Ensure unique IDs to avoid false mismatch counts
        unique_values = set(values)
        existing_ids = set(related_model.objects.filter(pk__in=unique_values).values_list("pk", flat=True))
        missing_ids = unique_values - existing_ids

        if missing_ids:
            self._handle_django_validation_error(
                DjangoValidationError(
                    {
                        field_name: (
                            f"The following IDs do not exist in {related_model.__name__}: {sorted(missing_ids)}"
                        )
                    }
                )
            )

    @transaction.atomic
    def create(self, schema, **kwargs):
        """Create a new model instance from schema data.

        Args:
            schema: Pydantic schema with model data.
            **kwargs: Additional arguments to pass to the model.

        Returns:
            The created model instance.

        Raises:
            ValidationError: If model validation fails.
            TypeError: If schema has invalid fields for the model.
        """
        context: RouteContext = service_resolver(RouteContext)
        data = schema.model_dump(by_alias=True)

        data.update(kwargs)

        m2m_data, data = self._separate_m2m_fields(data=data)

        try:
            instance = self.model(**data)
            # esta implementación es similar a lo que se hace en el modelo
            self._sync_display_name(instance)

            if self.pre_save:
                instance = self.pre_save(context.request, instance)

            # Ejecutar validadores de Django solo para los campos recibidos (RegexValidator, etc)
            self._validate_instance(instance)

            instance.save()

            # Now assign M2M
            for field_name, value in m2m_data.items():
                self._validate_m2m_options(instance=instance, field_name=field_name, values=value)
                m2m_manager = getattr(instance, field_name)
                m2m_manager.set(value)

            if self.post_save:
                instance = self.post_save(context.request, instance)

            return instance
        except TypeError as tex:  # pragma: no cover
            tb = traceback.format_exc()
            msg = (
                "Got a `TypeError` when calling `%s.%s.create()`. "
                "This may be because you have a writable field on the "
                "serializer class that is not a valid argument to "
                "`%s.%s.create()`. You may need to make the field "
                "read-only, or override the %s.create() method to handle "
                "this correctly.\nOriginal exception was:\n %s"
                % (
                    self.model.__name__,
                    self.model._default_manager.name,
                    self.model.__name__,
                    self.model._default_manager.name,
                    self.__class__.__name__,
                    tb,
                )
            )
            raise TypeError(msg) from tex

    @transaction.atomic
    def update(self, instance, schema, **kwargs):
        """Update an existing model instance with schema data.

        Args:
            instance: The model instance to update.
            schema: Pydantic schema with updated data.
            **kwargs: Additional arguments to merge into the update.

        Returns:
            The updated model instance.

        Raises:
            ValidationError: If model validation fails.
        """
        context: RouteContext = service_resolver(RouteContext)

        data = schema.model_dump(exclude_none=True, by_alias=True)
        data.update(kwargs)

        m2m_data, data = self._separate_m2m_fields(data=data)

        for attr, value in data.items():
            setattr(instance, attr, value)

        self._sync_display_name(instance)

        if self.pre_save:
            instance = self.pre_save(context.request, instance)

        # Ejecutar validadores de Django solo para los campos recibidos (RegexValidator, etc)
        self._validate_instance(instance)

        instance.save()

        # Now assign M2M
        for field_name, value in m2m_data.items():
            self._validate_m2m_options(instance=instance, field_name=field_name, values=value)
            m2m_manager = getattr(instance, field_name)
            m2m_manager.set(value)

        if self.post_save:
            instance = self.post_save(context.request, instance)

        return instance

    def delete(self, instance: Model, **kwargs: Any) -> Any:
        """Delete a model instance.

        Args:
            instance: The model instance to delete.
            **kwargs: Additional arguments (unused).

        Returns:
            The deleted model instance.
        """
        instance.delete()
        return instance

    def get_all(self, **kwargs):
        """Retrieve all model instances, optionally filtered.

        Applies filterset if configured and request parameters are valid.

        Args:
            **kwargs: Additional arguments to pass to parent get_all().

        Returns:
            QuerySet of model instances.
        """
        context: RouteContext = service_resolver(RouteContext)
        qs = super().get_all(**kwargs)
        if self.filterset_class:
            filterset_instance = self.filterset_class(context.request.GET, queryset=qs)
            if filterset_instance.is_valid():
                qs = filterset_instance.qs
        return qs

    def get_one(self, pk, **kwargs):
        """Retrieve a single model instance by primary key.

        Args:
            pk: The primary key of the instance to retrieve.
            **kwargs: Additional arguments to pass to get_all for filtering.

        Returns:
            The model instance.

        Raises:
            NotFound: If no instance with the given pk exists.
        """
        qs = self.get_all(**kwargs)
        kwargs.update({"queryset": qs})
        return super().get_one(pk=pk, **kwargs)
