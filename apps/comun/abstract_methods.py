from collections import defaultdict

from django.db.models import F, Q
from django.utils.timezone import now, timedelta
from safedelete.models import SafeDeleteModel


class AbstractMethodsMixin(SafeDeleteModel):
    """Abstract model that provides common functionality for controlled deletion and restoration.

    This class extends SafeDeleteModel and adds custom logic for:
    - Cascade deletion of related models (delete_on_cascade)
    - Deletion blocking when active children exist (child_relations)
    - Restoration blocking when parent records are deleted (parent_relations)
    - Automatic generation of unique names for display_name fields

    Class attributes:
        parent_relations (list): List of tuples defining parent relations that block restoration.
            Format: [("identifier_name", "related_query_name", "redirect_url")]
        child_relations (list): List of tuples defining child relations that block deletion.
            Format: [("identifier_name", "related_query_name", "redirect_url")]
        delete_on_cascade (list): List of related_query_name values to delete in cascade.
            Supports nested relations with "__" notation (e.g., "orden_venta__venta_producto").

    Usage example:
        class Producto(AbstractModel):
            delete_on_cascade = ["producto_abarrotes", "bodega_producto"]
            parent_relations = [("tipo productos", "tipo_producto", "productos:index")]
            child_relations = [("abarrotes", "producto_abarrotes", "abarrotes:index")]
    """

    parent_relations = []
    child_relations = []
    delete_on_cascade = []

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Automatically generate unique names for display_name fields.

        If the model has a 'display_name' field with a custom attribute that points to another field,
        this method automatically generates a unique name by appending a numeric suffix when needed.

        The display_name field must define a custom attribute indicating the target field name:
            display_name = models.CharField(max_length=150, display_name="tipo_producto", blank=True)

        Flow:
            1. Checks whether the model has a 'display_name' field.
            2. Reads the target field from the display_name custom attribute.
            3. If the target field already has a value, proceeds with the regular save.
            4. If it has no value, checks whether a record with the same prefix already exists.
            5. If it exists, appends a numeric suffix (_2, _3, etc.).

        Returns:
            None: Result of super().save().

        Example:
            If display_name = "Cámara" and "Cámara" already exists, it is saved as "Cámara_2".
        """
        # Check if model has a 'display_name' field and handle accordingly
        if not hasattr(self, "display_name"):
            return super().save(*args, **kwargs)

        display_name_field = self._meta.get_field("display_name")
        field_key = getattr(display_name_field, "display_name", None)

        # Proceed with default save if there's no display_name key or value
        if not field_key or getattr(self, field_key):
            return super().save(*args, **kwargs)

        # Fetch the current display name
        display_name = self.display_name

        # Get the number of records with display_name or starting with display_name
        count_records = self.__class__.objects.filter(**{f"{field_key}__startswith": display_name}).count()

        # If no records exist with the same display_name, set the original, else create a unique one
        new_display_name = display_name if count_records == 0 else f"{display_name}_{count_records + 1}"
        setattr(self, field_key, new_display_name)

        return super().save(*args, **kwargs)

    def _get_deepest_model(self, model, field_path):
        """Traverses nested relations to get the deepest model in a relation path.

        This helper is used by delete() and undelete() to find the final model
        in nested relation paths (e.g., "orden_venta__venta_producto" -> ProductoVenta).

        Args:
            model (Model): Starting model class where traversal begins.
            field_path (str): Relation path separated by "__".
                Example: "orden_venta__venta_producto"

        Returns:
            Model: The deepest model class in the relation chain.

        Example:
            >>> deepest_model = self._get_deepest_model(Orden, "orden_venta__venta_producto")
            >>> deepest_model.__name__
            'ProductoVenta'
        """
        fields = field_path.split("__")  # Split the delete_on_cascade path
        for field_name in fields:
            # Traverse the relationship to get the related model
            field = model._meta.get_field(field_name)
            if hasattr(field, "related_model"):
                model = field.related_model
            else:
                break
        return model

    def delete(self, *args, **kwargs):
        """Implement controlled cascade deletion.

          This method performs deletion in three steps:

          1. Check active children (child_relations):
              - If the record has active children, deletion is blocked.
              - Returns information about the child records preventing deletion.

          2. Cascade delete (delete_on_cascade):
              - Marks related records as deleted.
              - Supports nested relations using "__" notation.

          3. Delete the record:
              - Calls SafeDeleteModel's super().delete() (soft delete).

        Returns:
                tuple: On blocking, returns (False, {"blocking_info": [...], "delete": True}).
                         On success, returns the result of super().delete().

          blocking_info structure:
            {
                "blocking_info": [
                    {
                        "app_label": "abarrotes",
                        "model_name": "abarrote",
                        "model_str": "abarrotes",
                        "url_name": "abarrotes:index",
                        "elements": [<Abarrote 1>, <Abarrote 2>]
                    }
                ],
                "delete": True
            }

        Example:
            >>> producto = Producto.objects.get(id=1)
            >>> result = producto.delete()
            >>> # If it has active abarrotes:
            >>> # result = (False, {"blocking_info": [...], "delete": True})
            >>> # If it has no active children:
            >>> # Related abarrotes and warehouses are deleted, then the product.
        """
        blocking_info = []
        child_map = defaultdict(list)

        current_time = now()

        for model_str, relation, url in self.child_relations:
            filter_args = {"id": self.id, f"{relation}__deleted__isnull": True}

            if self.__class__.objects.filter(**filter_args).exists():
                child_ids = list(
                    self.__class__.objects.filter(**filter_args).values_list(f"{relation}__id", flat=True).distinct()
                )

                # Remove None values in Python
                child_ids = [id for id in child_ids if id is not None]

                if not child_ids:  # Now this will work correctly
                    continue

                related_model = self._get_deepest_model(self.__class__, relation)

                active_children = related_model.objects.filter(id__in=child_ids)
                child_map[(model_str, relation, url)].extend(active_children)

        if child_map:
            grouped = defaultdict(
                lambda: {
                    "app_label": None,
                    "model_name": None,
                    "relation": None,
                    "elements": [],
                    "url_name": None,
                }
            )

            for (model_str, relation, url), elements in child_map.items():
                app_label = None
                model_name = None
                model_str = model_str
                url = url

                if elements:
                    element = elements[0]
                    related_model = element.__class__
                    app_label = related_model._meta.app_label
                    model_name = related_model._meta.model_name

                key = (model_str, relation)
                if grouped[key]["app_label"] is None:
                    grouped[key]["app_label"] = app_label
                    grouped[key]["model_name"] = model_name
                    grouped[key]["model_str"] = model_str
                    grouped[key]["url_name"] = url

                grouped[key]["elements"].extend(elements)

            blocking_info = list(grouped.values())
            return False, {"blocking_info": blocking_info, "delete": True}

        # Verificar que los hijos en todos los niveles estén eliminados
        for delete_on_cascade in self.delete_on_cascade:
            # # Example delete_on_cascade could be 'movie_sale__sale__order' or 'movie_sale'
            # delete_on_cascade = "movie_sale__sale__order"  # Dynamic field

            # Split and traverse to get the deepest related model
            deepest_model = self._get_deepest_model(self.__class__, delete_on_cascade)

            # Run your query to get the IDs dynamically, as before
            filter_query = {"id": self.id, f"{delete_on_cascade}__deleted__isnull": True}

            ids_to_delete = (
                self.__class__.objects.annotate(ids_to_delete=F(f"{delete_on_cascade}__id"))
                .filter(
                    **filter_query,
                )
                .values_list("ids_to_delete", flat=True)
            )
            deepest_model.objects.filter(id__in=ids_to_delete).update(deleted=current_time)

        # Step 3: Call the parent delete method to delete the object itself
        return super().delete(*args, **kwargs)

    def undelete(self, *args, **kwargs):
        """Implement controlled cascade restoration.

          This method performs restoration in three steps:

          1. Check deleted parents (parent_relations):
              - If the record has deleted parents, restoration is blocked.
              - Returns information about parent records preventing restoration.

          2. Cascade restore (delete_on_cascade):
              - Restores related records deleted at the same time.
              - Uses a ±500ms time window to determine which records to restore.

          3. Restore the record:
              - Calls SafeDeleteModel's super().undelete().

          The time window ensures only records deleted together with the parent
          (in the same operation) are restored, avoiding restoration of records
          that were independently deleted earlier.

        Returns:
                tuple: On blocking, returns (False, {"blocking_info": [...], "delete": False}).
                         On success, returns the result of super().undelete().

          blocking_info structure:
            {
                "blocking_info": [
                    {
                        "app_label": "tipo_productos",
                        "model_name": "tipoproducto",
                        "model_str": "tipo productos",
                        "url_name": "productos:index",
                        "elements": [<TipoProducto 1>]
                    }
                ],
                "delete": False
            }

        Example:
            >>> producto = Producto.all_objects.get(id=1)
            >>> result = producto.undelete()
            >>> # If tipo_producto is deleted:
            >>> # result = (False, {"blocking_info": [...], "delete": False})
            >>> # If tipo_producto is active:
            >>> # Deleted abarrotes and warehouses are restored, then the product.
        """
        blocking_info = []
        child_map = defaultdict(list)
        # Verificar que los padres en todos los niveles estén restaurados
        for model_str, parent_relation, url in self.parent_relations:
            filter_args = {"id": self.id, f"{parent_relation}__deleted__isnull": False}

            if self.__class__.all_objects.filter(**filter_args).exists():
                parent_ids = list(
                    self.__class__.all_objects.filter(**filter_args)
                    .values_list(f"{parent_relation}__id", flat=True)
                    .distinct()
                )

                # Remove None values in Python
                parent_ids = [id for id in parent_ids if id is not None]

                if not parent_ids:
                    continue

                related_model = self._get_deepest_model(self.__class__, parent_relation)

                active_children = related_model.all_objects.filter(id__in=parent_ids)
                child_map[(model_str, parent_relation, url)].extend(active_children)

        if child_map:
            grouped = defaultdict(
                lambda: {
                    "app_label": None,
                    "model_name": None,
                    "relation": None,
                    "elements": [],
                    "url_name": None,
                }
            )

            for (model_str, relation, url), elements in child_map.items():
                app_label = None
                model_name = None
                model_str = model_str
                url = url

                if elements:
                    element = elements[0]
                    related_model = element.__class__
                    app_label = related_model._meta.app_label
                    model_name = related_model._meta.model_name

                key = (model_str, relation)
                if grouped[key]["app_label"] is None:
                    grouped[key]["app_label"] = app_label
                    grouped[key]["model_name"] = model_name
                    grouped[key]["model_str"] = model_str
                    grouped[key]["url_name"] = url

                grouped[key]["elements"].extend(elements)

            blocking_info = list(grouped.values())
            return False, {"blocking_info": blocking_info, "delete": False}
        # Restaurar los hijos en cascada
        for delete_on_cascade in self.delete_on_cascade:
            # Get the deepest related model
            deepest_model = self._get_deepest_model(self.__class__, delete_on_cascade)

            # Retrieve the IDs of related records that are marked as deleted
            filter_q = Q(
                id=self.id,
                **{f"{delete_on_cascade}__deleted__isnull": False},
            )

            ids_to_restore = (
                self.__class__.all_objects.annotate(ids_to_restore=F(f"{delete_on_cascade}__id"))
                .filter(filter_q)
                .values_list("ids_to_restore", flat=True)
            )

            # half second buffer
            time_buffer = timedelta(milliseconds=500)
            deleted_at = self.deleted

            start_date = deleted_at - time_buffer
            end_date = deleted_at + time_buffer

            query = Q(id__in=ids_to_restore, deleted__gte=start_date, deleted__lte=end_date)
            # Restore the records in the deepest related model by setting deleted=False
            deepest_model.deleted_objects.filter(query).update(deleted=None)

        # Call the parent's undelete method and return its result
        return super().undelete(*args, **kwargs)
