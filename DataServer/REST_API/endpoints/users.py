from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from ..serializer import UserSerializer
from rest_framework.authtoken.models import Token
from ..models import Setting


class Register(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User(
                username=serializer.validated_data['username'])
            user.set_password(serializer.validated_data['password'])
            user.save()
            token = Token.objects.create(user=user)

            Setting.objects.create(user=user)

            return Response(status=200, data=token.key)
        return Response(status=400, data="A user with that username already exists.")


# Get Token for User
class Login(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            print(e)
            return Response(status=400, data="Wrong username or password")

        if (user.check_password(password) == True):
            token = Token.objects.get(user=user)
            return Response(status=200, data=token.key)

        return Response(status=400, data="Wrong username or password")
