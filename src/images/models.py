from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from likes.models import Like

class Image(models.Model):
    picture = models.ImageField(
        "Картинка",
        upload_to='images/%Y/%m/%d',
    )
    body = models.CharField(
        max_length=25,
        verbose_name='Название картинки',
    )

    likes = GenericRelation(Like)

    def __str__(self):
        return self.body

    @property
    def total_likes(self):
        return self.likes.count()
    
    class Meta:
        verbose_name="Image"
        verbose_name_plural="Images"
