class PlantViewMixin:
    """
    Mixin for common functionality against all plant views.
    """

    context_object_name = "plant"

    def get_queryset(self):
        """
        Ensures that users can only see their own plants.
        """
        return super().get_queryset().filter(user=self.request.user)
