from rest_framework.routers import DefaultRouter
from .views import ImageViewSet, Top5ViewSet, RandomViewSet

# Создаем router и регистрируем ViewSet
router = DefaultRouter()
router.register(r'images', ImageViewSet, basename='images')
router.register(r'top5', Top5ViewSet, basename='top5')
router.register(r'random', RandomViewSet, basename='random')
# URLs настраиваются автоматически роутером
urlpatterns = router.urls