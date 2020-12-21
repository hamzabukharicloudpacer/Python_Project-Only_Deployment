class MultipleSerializersViewSetMixin:

    def get_serializers(self):
        return self.serializers if hasattr(self, 'serializers') else {}

    def get_serializer_class(self, *args, **kwargs):
        default_serializer = super().get_serializer_class(*args, **kwargs)
        serializers = self.get_serializers()
        return serializers.get(self.action, default_serializer)
