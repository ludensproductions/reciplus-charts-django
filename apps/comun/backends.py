from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import Permission
from django.db.models import Q


class CustomModelBackend(ModelBackend):
    def _get_group_permissions(self, user_obj):
        # Obtener atributos o en su defecto None
        user_departamento = getattr(user_obj, "departamento", None)
        user_puesto = getattr(user_obj, "puesto", None)

        base_condition = Q(group__customgroup__deleted__isnull=True)

        user_groups_q = Q(
            group__customgroup__groups_users__user=user_obj.id,
            group__customgroup__groups_users__deleted__isnull=True,
            group__customgroup__groups_users__user__deleted__isnull=True,
        )

        user_departamento_q = Q()
        if user_departamento:
            user_departamento_q = Q(
                group__customgroup__departamento_groups__departamento=user_departamento,
                group__customgroup__departamento_groups__deleted__isnull=True,
                group__customgroup__departamento_groups__departamento__deleted__isnull=True,
            )

        user_puesto_q = Q()
        if user_puesto and user_departamento:
            user_puesto_q = Q(
                group__customgroup__group_puesto_departamento__puesto_departamento__puesto=user_puesto,
                group__customgroup__group_puesto_departamento__puesto_departamento__departamento=user_departamento,
                group__customgroup__group_puesto_departamento__deleted__isnull=True,
                group__customgroup__group_puesto_departamento__puesto_departamento__deleted__isnull=True,
                group__customgroup__group_puesto_departamento__puesto_departamento__puesto__deleted__isnull=True,
                group__customgroup__group_puesto_departamento__puesto_departamento__departamento__deleted__isnull=True,
            )

        # Combinar las condiciones con OR y retornar el user_permissions
        filter_conditions = user_groups_q | user_departamento_q | user_puesto_q
        user_permissions = Permission.objects.filter(base_condition & filter_conditions).distinct()

        return user_permissions
