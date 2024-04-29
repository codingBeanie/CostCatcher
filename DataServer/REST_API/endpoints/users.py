from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from ..serializer import UserSerializer
from rest_framework.authtoken.models import Token
from ..models import Setting


class Register(APIView):
    def post(self, request):
        print("API REGISTER:", request.data)
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

# Update Password


class UpdatePassword(APIView):
    def put(self, request):
        user = request.user
        currentPassword = request.data['currentPassword']
        newPassword = request.data['newPassword']

        if user.check_password(currentPassword):
            user.set_password(newPassword)
            user.save()
            return Response(status=200, data="Password Updated")
        return Response(status=400, data="Wrong password")


class DeleteUser(APIView):
    def delete(self, request):
        user = request.user
        user.delete()
        return Response(status=200, data="User Deleted")
