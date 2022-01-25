from django.contrib import admin
from . import models

class ImageAdmin(admin.ModelAdmin):
    list_display=[
    'picture', 
    'body',
    'likes',
    'total_likes',
    ]

admin.site.register(models.Image, ImageAdmin)
