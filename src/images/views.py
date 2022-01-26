from rest_framework import viewsets
from rest_framework import permissions 
from .models import Image
from .serializers import ImageSerializer
from likes.mixins import LikedMixin, ReportedMixin
from django.db.models import Count, Max
import random

class ImageViewSet(LikedMixin, ReportedMixin, viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class Top5ViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all().annotate(cnt=Count('likes')).order_by('-cnt')[0:5]
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class RandomViewSet(LikedMixin, ReportedMixin, viewsets.ModelViewSet):
    queryset = Image.objects.alias(cnt=Count('reports')).filter(cnt__lt=1).order_by('?')
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]