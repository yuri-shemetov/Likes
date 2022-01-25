from rest_framework import serializers
from likes import services as likes_services

from .models import Image

class ImageSerializer(serializers.ModelSerializer):
    is_fan = serializers.SerializerMethodField()
    is_report = serializers.SerializerMethodField()
    class Meta:
        model = Image
        fields = (
            'id',
            'picture',
            'body',
            'is_fan',
            'is_report',
            'total_likes',
            'total_reports',
        )

    def get_is_fan(self, obj) -> bool:
        """Проверяет, лайкнул ли `request.user` картинку (`obj`).
        """
        user = self.context.get('request').user
        return likes_services.is_fan(obj, user)

    def get_is_report(self, obj) -> bool:
        """Проверяет, сделал ли `request.user` репорт картинки (`obj`).
        """
        user = self.context.get('request').user
        return likes_services.is_report(obj, user)