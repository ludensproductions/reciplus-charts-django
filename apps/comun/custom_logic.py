# The class `UtilsClass` contains a static method `pre_save` that sets the `created_by`
# or `updated_by` fields of an instance based on whether it is being created or updated.
class UtilsClass:
    @staticmethod
    def pre_save(request, instance, *args, **kwargs):
        if instance.id is None:
            instance.created_by = request.user
        else:
            instance.updated_by = request.user

        return instance

    @staticmethod
    def filter_queryset(model, query_parameters: dict = None):
        if not query_parameters:
            query_parameters = {}

        # if path parameters are not in the model fields, remove them
        query_parameters = {key: value for key, value in query_parameters.items() if hasattr(model, key)}

        # Convert path parameters to query parameters
        query_parameters = {key: value for key, value in query_parameters.items()}

        query = model.objects.filter(**query_parameters)

        return query
