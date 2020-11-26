from rest_framework import viewsets

from images.models import TemplateStore
from images.serializers import TemplateStoreSerializer


class TemplateStoreViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing templates
    """

    queryset = TemplateStore.objects.all()
    serializer_class = TemplateStoreSerializer
    pagination_class = None
