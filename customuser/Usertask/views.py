from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated 
from django.contrib.auth import authenticate
from django.contrib.auth.models import User ,  Permission
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework import status
from Usertask.models import Task , TaskUser
from Usertask.serializer import TaskSerializer , TaskUserSerializer
from customuser.utils import AdminRequired , ManagerRequired



class TaskList(APIView):
    permission_classes = (IsAuthenticated,AdminRequired)
    def get(self , request):
        user = self.request.user
        todo_task = Task.objects.all()
        serializer = TaskSerializer(todo_task, many=True)
        return Response(serializer.data)
    
    def post(self , request):
        title = request.data.get("title")
        if Task.objects.filter(title=title).exists():
            return Response("task already exists")
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
        
    
    
class TaskDetail(APIView):
    permission_classes = (IsAuthenticated,AdminRequired)
    def get(self, request, pk, format=None):
        log_task = Task.objects.get(pk=pk)
        if log_task is None:
            return Response("task not found")
        serializer = TaskSerializer(log_task)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        task = Task.objects.get(pk=pk)
        serializer = TaskSerializer(task,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        task = Task.objects.get(pk=pk)
        task.delete()
        return Response({
                    'status': 'success',
                    'message': 'task deleted',
                })
class TaskAssignAdmin(APIView):
    permission_classes = (IsAuthenticated,AdminRequired)
    def post(self , request):
        taskID = request.data.get("taskID")
        userEmail = request.data.get("userEmail")
        if TaskUser.objects.filter(taskID=taskID).exists():
            taskID = TaskUser.objects.filter(taskID=taskID)
            check_usermail = [item.userEmail for item in taskID]
            for x in check_usermail :
                if userEmail == x:
                    return Response("this task is already assign to this user")
        serializer = TaskUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self , request):
        todo_task = TaskUser.objects.all()
        serializer = TaskUserSerializer(todo_task, many=True)
        return Response(serializer.data)    

class TaskAssignManager(APIView):
    permission_classes = (IsAuthenticated,ManagerRequired)
    def post(self , request):
        serializer = TaskUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self , request):
        todo_task = TaskUser.objects.all()
        serializer = TaskUserSerializer(todo_task, many=True)
        return Response(serializer.data)    



#user can find his tasks #
class TaskAssignGet(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self , request ,format=None ):
        email = request.user.email
        users_task = TaskUser.objects.filter(userEmail=email)
        serializer = TaskUserSerializer(users_task, many=True)
        return Response(serializer.data)
    
    
class TaskInfo(APIView):
    def get(self, request, pk, format=None):
            
        log_task = Task.objects.get(pk=pk)
        serializer = TaskSerializer(log_task)
        return Response(serializer.data)


class BulkDeleteTask(APIView):
    permission_classes = (IsAuthenticated,AdminRequired)
    def post(self, request, *args, **kwargs):
        delete_ids = request.data.get("delete_ids")
        ID=[x for x in delete_ids]
        for i in ID:
            check=Task.objects.filter(pk=i).delete()
        return Response("All task deleted")
    
class BulkAddTask(APIView):
    permission_classes = (IsAuthenticated,AdminRequired)
    def post(self, request,):
        task= request.data.get("tasks")
        for i in task:
            serializer = TaskSerializer(data=i)
            if serializer.is_valid():
                serializer.save()
        return Response("Tasks Created Successfully")
        