from django.shortcuts import render
from Accounts.serializer import UserSerializered ,ChangePasswordSerializer , AssignRoleSerializer,UpdateSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework import status
from Accounts.models import MyUser
from django.contrib.auth import get_user_model 
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from customuser.utils import EMAIL_HOST_USER , url_api
import base64
import uuid
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives





class UseRegister(APIView):
    """
    Create user 
    """

    def post(self, request):
        username=request.data.get("username")
        if MyUser.objects.filter(username=username).exists():
            return Response("username already exist")
        email=request.data.get("email")
        if MyUser.objects.filter(email=email).exists():
            return Response("email exist")
        phone_number=request.data.get("phone_already number")
        if MyUser.objects.filter(phone_number=phone_number).exists():
            return Response("phone_number already exist")
        role=request.data.get("role")
        if role =="Admin" or role=="Manager":
            return Response("User Can't Use Administration Role")
        
        user= MyUser.objects.create_user(
            role=request.data.get("role"),
            email=request.data.get("email"),
            username=request.data.get("username"),
            first_name=request.data.get("first_name"),
            last_name=request.data.get("last_name"),
            password=request.data.get("password"),
            phone_number=request.data.get("phone_number"),
            address=request.data.get("address"))
        user.save()
        if user is not None:
            token = Token.objects.create(user=user)
            return Response(token.key)
        else:
            return Response(["BAD_REQUEST"], status=status.HTTP_400_BAD_REQUEST)
        
class UserProfile(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        user = UserSerializered(request.user)
        return Response(user.data)


class UserLogin(APIView):
    
    def post(self, request):
        user = authenticate(username=request.data.get(
            "username"), password=request.data.get("password"))
        if user is not None:
            try:
                token = Token.objects.get(user_id=user.id)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)
            return Response(token.key)
        else:
            return Response({"Unauthorized":["Wrong username or password"]}, status=status.HTTP_401_UNAUTHORIZED)

class ChangePasswordView(APIView):
        permission_classes = [IsAuthenticated]
        def post(self, request):
            log_username = self.request.user
            serializer = ChangePasswordSerializer(data=request.data)

            if serializer.is_valid():
                old_password = serializer.data.get("old_password")
                new_password =serializer.data.get("new_password")
                confirm_new_password=serializer.data.get("confirm_new_password")
                # Check old password
                if not log_username.check_password(serializer.data.get("old_password")):
                    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                # match password
                if new_password !=confirm_new_password:
                    return Response({"Password Match":["Password did not match"]}, status=status.HTTP_400_BAD_REQUEST)
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                return Response({
                        'status': 'success',
                        'message': 'Password updated successfully',
                    })


class ForgotPassword(APIView):
    def post(self,request):
        email = request.data.get("email")
        if MyUser.objects.filter(email=email).exists():
            pass
        else:
            return Response("email dose not exist")
        string_bytes = email.encode("ascii")
        base64_bytes = base64.b64encode(string_bytes)
        encode_mail = base64_bytes.decode("ascii")
        
        #mail details#
        subject = "welcome solution wolrd"
        html_content= url_api.replace("{{DATA}}",str(encode_mail))
        message = "Forgot password request found"
        from_email = EMAIL_HOST_USER
        if subject and message and from_email:
            try:
                msg = EmailMultiAlternatives(subject, message, from_email, [email])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return Response({"Mail_Send":["Send successfully"]})
        else:
            return Response('Make sure all fields are entered and valid.')
        
        


class TempPassword(APIView):
    def get(self, request):
        email = request.GET.get("Email")
        base64_bytes = email.encode("ascii")
        sample_string_bytes = base64.b64decode(base64_bytes)
        sample_string = sample_string_bytes.decode("ascii")
        email = sample_string
        user = MyUser.objects.get(email=email)
        passwod = uuid.uuid4().hex
        user.set_password(passwod)
        user.save()
        subject = 'welcome solution world'
        message = f'Hi -- {passwod}, is your temp password , make a new one '
        email_from = EMAIL_HOST_USER
        recipient_list = [email, ]
        if subject and message and email_from:
            try:
                send_mail( subject, message, email_from, recipient_list )
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return Response({"Mail_Send":["Send successfully"]})
        else:
            return HttpResponse('Make sure all fields are entered and valid.')
        return Response(str(user))
    
    
class DeleteUserView(APIView):
    permission_classes = (IsAuthenticated,)
    def delete(self, request , pk):
        role = self.request.user.role
        if role =="Admin" :
            user = self.request.get(pk=pk)
            user.delete()
            return Response({
                            'status': 'success',
                            'code': status.HTTP_200_OK,
                            'message': 'delete updated successfully',
                        })
        return Response({"unauthorised"},status=403)
    
    
class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request):
        log_username = self.request.user
        serializer = UpdateSerializer(log_username,data=self.request.data)
        username=request.data.get("username")
        if MyUser.objects.filter(username=username).exists():
            return Response("username already exists")
        phone_number=request.data.get("phone_number")
        if MyUser.objects.filter(phone_number=phone_number).exists():
            return Response("phone_number already exists")
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({"Not Valid": ["BAD_REQUEST"]}, status=status.HTTP_400_BAD_REQUEST)


class AssignUserRole(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        role = self.request.user.role
        if role =="Admin":
            user = MyUser.objects.get(pk=pk)
            check_role = self.request.user.role
            print("##########",check_role)
            if check_role=="Manager":
                return Response("already Manager")
            serializer = AssignRoleSerializer(user,data=self.request.data)
            if serializer.is_valid():
                serializer.save()
            return Response({
                            'status': 'success',
                            'message': "{{user}}assign as Manager" ,
                        })
        else:
            return Response("Role Assign Criteria Not Valid")
    
