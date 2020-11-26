from rest_framework import serializers

from images.models import TemplateStore


class TemplateStoreSerializer(serializers.ModelSerializer):
    """
    A simple Model serializer for TemplateStore
    """

    class Meta:
        model = TemplateStore
        fields = '__all__'
