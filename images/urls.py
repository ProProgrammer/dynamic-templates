from rest_framework.routers import DefaultRouter

from images.views import TemplateStoreViewSet

router = DefaultRouter()
router.register(r'templates', TemplateStoreViewSet, basename='template')
urlpatterns = router.urls
