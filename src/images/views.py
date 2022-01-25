from rest_framework import viewsets
from rest_framework import permissions 
from .models import Image
from .serializers import ImageSerializer
from likes.mixins import LikedMixin

class ImageViewSet(LikedMixin, viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    #permission_classes = (permissions.AllowAny,)