from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Setting
from ..serializer import SettingsSerializer


class Settings(APIView):
    def get(self, request):
        data = Setting.objects.first()
        serializer = SettingsSerializer(data)
        return Response(status=200, data=serializer.data)

    def put(self, request):
        data = request.data
        settings = Setting.objects.first()
        serializer = SettingsSerializer(settings, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200, data="Settings have been updated")
        return Response(status=500, data="Settings could not be updated")
