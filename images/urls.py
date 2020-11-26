from django.urls import path
from rest_framework.routers import DefaultRouter

from images.views import TemplateStoreViewSet, ImageGenerationView

router = DefaultRouter()
router.register(r'templates', TemplateStoreViewSet, basename='template')
urlpatterns = router.urls

urlpatterns += [
    path('image-service/', ImageGenerationView.as_view()),
]
