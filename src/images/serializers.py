from rest_framework import serializers
from likes import services as likes_services

from .models import Image

class ImageSerializer(serializers.ModelSerializer):
    is_fan = serializers.SerializerMethodField()
    class Meta:
        model = Image
        fields = (
            'id',
            'picture',
            'body',
            'is_fan',
            'total_likes'
        )

    def get_is_fan(self, obj) -> bool:
        """Проверяет, лайкнул ли `request.user` твит (`obj`).
        """
        user = self.context.get('request').user
        return likes_services.is_fan(obj, user)
