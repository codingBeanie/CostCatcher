from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from ..serializer import UserSerializer
from rest_framework.authtoken.models import Token
from ..models import Setting
from django.core.mail import send_mail
import logging


class Register(APIView):
    def post(self, request):
        try:

            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = User(
                    username=serializer.validated_data['username'])
                user.set_password(serializer.validated_data['password'])
                user.email = serializer.validated_data['email']
                user.save()
                token = Token.objects.create(user=user)

                Setting.objects.create(user=user)

                return Response(status=200, data=token.key)
            return Response(status=400, data="A user with that username already exists.")
        except Exception as e:
            logging.getLogger('costcatcher').error(e)
            return Response(status=500, data="An error occured")


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
            responseData = {}
            responseData['token'] = token.key
            responseData['email'] = user.email
            return Response(status=200, data=responseData)

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


class SetNewPassword(APIView):
    def put(self, request):
        try:
            user = request.user
            user.set_password(request.data['password'])
            user.save()
            return Response(status=200, data="Password Updated")
        except Exception as e:
            logging.getLogger('costcatcher').error(e)
            return Response(status=400, data="Could not update password")


class UpateEmail(APIView):
    def put(self, request):
        try:
            user = request.user
            user.email = request.data['email']
            user.save()
            return Response(status=200, data="Email Updated")
        except Exception as e:
            logging.getLogger('costcatcher').error(e)
            return Response(status=400, data="Could not update email")


class RequestPasswordReset(APIView):
    def post(self, request):
        try:
            user = User.objects.get(username=request.data['username'])
            if user is None:
                logging.getLogger('costcatcher').error(
                    "Password Rest: User not found:" + request.data['username'])
                return Response(status=200, data="Password Reset Email Sent")

            token = Token.objects.get(user=user)
            message = "Dear " + user.username + ",\n\n" + \
                "you requested a password reset for Costcatcher. Click the link to reset your password\n\n" + \
                "https://costcatcher.cbeanie.com/resetpassword/" + str(token) +  \
                "\n\n" + "Costcatcher Team" + "\n\n\n\n" + \
                "This is an automated email. Please do not reply to this email."

            send_mail(
                'Password Reset',
                message,
                'mail@costcatcher.cbeanie.com',
                [user.email],
                fail_silently=False,)

        except Exception as e:
            logging.getLogger('costcatcher').error(e)
            return Response(status=400, data="Could not send email")

        logging.getLogger('costcatcher').info(
            "Password Reset Email Sent to " + user.email)
        return Response(status=200, data="Password Reset Email Sent")


class DeleteUser(APIView):
    def delete(self, request):
        user = request.user
        user.delete()
        return Response(status=200, data="User Deleted")
