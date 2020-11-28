from django.urls import path
from rest_framework.routers import DefaultRouter

from images.views import TemplateStoreViewSet, ImageGenerationView, DataFeedGenerationView

router = DefaultRouter()
router.register(r'templates', TemplateStoreViewSet, basename='template')
urlpatterns = router.urls

app_name = 'images'

urlpatterns += [
    path('image-service/', ImageGenerationView.as_view(), name='image_generation_service'),
    path('generate-data-feed/', DataFeedGenerationView.as_view(), name='generate_data_feed'),
]
