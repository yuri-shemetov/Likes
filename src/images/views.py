from rest_framework import viewsets, permissions
from .models import Image
from .serializers import ImageSerializer
from likes.mixins import LikedMixin, ReportedMixin
from django.db.models import Count
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
    list_id = [i.id for i in Image.objects.alias(cnt=Count('reports')).filter(cnt__lt=1)]
    random.shuffle(list_id)
    clauses = ' '.join(['WHEN id=%s THEN %s' % (pk, i) for i, pk in enumerate(list_id)])
    ordering = 'CASE %s END' % clauses
    queryset = Image.objects.filter(pk__in=list_id).extra(
        select={'ordering': ordering}, order_by=('ordering',))
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]