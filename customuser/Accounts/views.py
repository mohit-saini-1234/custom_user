from django.shortcuts import render
from Accounts.serializer import UserSerializered ,ChangePasswordSerializer , AssignRoleSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework import status
from Accounts.models import MyUser
from django.contrib.auth import get_user_model 
from customuser.utils import AdminRequired , ManagerRequired 
from rest_framework.permissions import IsAuthenticated 
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
        phone=request.data.get("phone")
        if MyUser.objects.filter(phone=phone).exists():
            return Response("phone already exist")
        check_role= MyUser.objects.filter(role="Admin").count()
        role=request.data.get("role")
        if check_role>0 and role =="Admin" :
            return Response("User Can't Use Administration Role")
        if role =="Manager":
            return Response("User Can't Use Manager Role")
        
        user= MyUser.objects.create_user(
            role=request.data.get("role"),
            email=request.data.get("email"),
            username=request.data.get("username"),
            first_name=request.data.get("first_name"),
            last_name=request.data.get("last_name"),
            password=request.data.get("password"),
            phone=request.data.get("phone"),
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
    
    
class DeleteUserAdmin(APIView):
    permission_classes = (IsAuthenticated,AdminRequired)
    def delete(self, request , pk):
        try:
            user = MyUser.objects.get(pk=pk)
            if user is None:
                return Response("user not valid")
            user.delete()
            return Response({
                            'status': 'success',
                            'code': status.HTTP_200_OK,
                            'message': 'delete updated successfully',
                        })
        except MyUser.DoesNotExist:
            return Response("user not found ",status=404)
class DeleteUserManager(APIView):
    permission_classes = (IsAuthenticated,ManagerRequired)
    def delete(self, request , pk):
        try:
            user = MyUser.objects.get(pk=pk)
            if user.role=="Admin" or user.role=="Manager":
                return Response({"Unauthorised":"Can't delete Admin or Manager"})
            if user is None:
                return Response("user not valid")
            user.delete()
            return Response({
                            'status': 'success',
                            'code': status.HTTP_200_OK,
                            'message': 'delete updated successfully',
                        })
        except MyUser.DoesNotExist:
            return Response("user not found ",status=404)
        
class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request):
        user = self.request.user
        serializer = UserSerializered(user,data=request.data,partial=True)
        username=request.data.get("username")
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
            


class AssignUserRole(APIView):
    permission_classes = [IsAuthenticated, AdminRequired,]
    def put(self, request, pk):
        role_value=request.data.get("role")
        user = MyUser.objects.get(pk=pk)
        serializer = AssignRoleSerializer(user,data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                            'status': 'success',
                            'message': "__"+str(user)+"__assign as__"+str(role_value)+"__" 
                        })
        else:
            return Response("Role Assign Criteria Not Valid")
    
