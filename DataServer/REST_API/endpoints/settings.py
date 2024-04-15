from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Setting
from ..serializer import SettingsSerializer


class Settings(APIView):
    def get(self, request):
        settings = Setting.objects.get(user=request.user)
        serializer = SettingsSerializer(settings)
        return Response(status=200, data=serializer.data)

    def put(self, request):
        data = request.data
        data['user'] = request.user.id
        settings = Setting.objects.get(user=request.user)
        serializer = SettingsSerializer(settings, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200, data="Settings have been updated")
        print(serializer.errors)
        return Response(status=500, data=serializer.errors)
