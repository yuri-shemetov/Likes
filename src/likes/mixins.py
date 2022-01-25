from rest_framework.decorators import action
from rest_framework.response import Response
from . import services
from .serializers import FanSerializer, ReportSerializer


class LikedMixin:
    @action(detail=True, methods=['POST', 'GET'])
    def like(self, request, pk=None):
        """Лайкает `obj`.
        """
        obj = self.get_object()
        services.add_like(obj, request.user)
        return Response()

    @action(detail=True, methods=['POST', 'GET'])
    def unlike(self, request, pk=None):
        """Удаляет лайк с `obj`.
        """
        obj = self.get_object()
        services.remove_like(obj, request.user)
        return Response()

    @action(detail=True, methods=['POST', 'GET'])
    def fans(self, request, pk=None):
        """Получает всех пользователей, которые лайкнули `obj`.
        """
        obj = self.get_object()
        fans = services.get_fans(obj)
        serializer = FanSerializer(fans, many=True)
        return Response(serializer.data)

class ReportedMixin:
    @action(detail=True, methods=['POST', 'GET'])
    def report(self, request, pk=None):
        """Делает репорт `obj`.
        """
        obj = self.get_object()
        services.add_report(obj, request.user)
        return Response()

    @action(detail=True, methods=['POST', 'GET'])
    def unreport(self, request, pk=None):
        """Удаляет репорт с `obj`.
        """
        obj = self.get_object()
        services.remove_report(obj, request.user)
        return Response()

    @action(detail=True, methods=['POST', 'GET'])
    def reports(self, request, pk=None):
        """Получает всех пользователей, которые сделали репорт `obj`.
        """
        obj = self.get_object()
        reports = services.get_reports(obj)
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data)