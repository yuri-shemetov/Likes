from rest_framework.routers import DefaultRouter
from .views import ImageViewSet

# Создаем router и регистрируем ViewSet
router = DefaultRouter()
router.register(r'images', ImageViewSet)
# URLs настраиваются автоматически роутером
urlpatterns = router.urls