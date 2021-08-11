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
from Accounts.models import MyUser



class AllTaskListAdmin(APIView):
    permission_classes = (IsAuthenticated,AdminRequired)
    def get(self , request):
        todo_task = Task.objects.all()
        serializer = TaskSerializer(todo_task, many=True)
        return Response(serializer.data)

class AllAssignTaskListAdmin(APIView):
    permission_classes = (IsAuthenticated,AdminRequired)
    def get(self , request):
        todo_task = TaskUser.objects.all()
        serializer = TaskUserSerializer(todo_task, many=True)
        return Response(serializer.data)

    



class TaskListAdmin(APIView):
    permission_classes = (IsAuthenticated,AdminRequired)
    def get(self , request):
        user = self.request.user
        # admin = MyUser.objects.get(username=user) # remove this
        todo_task = Task.objects.filter(creator_ID=user)
        serializer = TaskSerializer(todo_task, many=True)
        return Response(serializer.data)

    def post(self , request):
        title = request.data.get("title")
        # if Task.objects.filter(title=title).exists(): # remove this..
        #     return Response("task already exists")
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            user= request.user
            serializer.save(creator_ID=user,Creator_username=user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class TaskListManager(APIView):
    permission_classes = (IsAuthenticated,ManagerRequired)
    def get(self , request):
        user = self.request.user
        # Manager = MyUser.objects.get(username=user) # remove 
        todo_task = Task.objects.filter(creator_ID=user)
        serializer = TaskSerializer(todo_task, many=True)
        return Response(serializer.data)

    def post(self , request):
        title = request.data.get("title")
        # if Task.objects.filter(title=title).exists(): # remove
        #     return Response("task already exists")
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            user= request.user
            serializer.save(creator_ID=user,Creator_username=user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class TaskDetailAdmin(APIView):
    permission_classes = (IsAuthenticated,AdminRequired)
    def get(self, request, pk, format=None):
        try:
            log_task = Task.objects.get(pk=pk)
            serializer = TaskSerializer(log_task)
            return Response(serializer.data)
        except Task.DoesNotExist:
            return Response('Not found', status=404)
        

    def put(self, request, pk, format=None):
        try:
            task = Task.objects.get(pk=pk)
            serializer = TaskSerializer(task,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Task.DoesNotExist:
            return Response('Not found', status=404)
    def delete(self, request, pk, format=None):
        try:
            task = Task.objects.get(pk=pk)
            task.delete()
            return Response({
                    'status': 'success',
                    'message': 'task deleted',
                })
        except Task.DoesNotExist:
            return Response('Not found', status=404)
        

        
        

        
class TaskDetailManager(APIView):
    permission_classes = (IsAuthenticated,ManagerRequired)
    def get(self, request, pk, format=None):
        try:
            log_task = Task.objects.get(pk=pk)
            serializer = TaskSerializer(log_task)
            return Response(serializer.data)
        except Task.DoesNotExist:
            return Response('Not found', status=404)
        
    def put(self, request, pk, format=None):
        try:
            task = Task.objects.get(pk=pk)
            serializer = TaskSerializer(task,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Task.DoesNotExist:
            return Response('Not found', status=404)
        
    def delete(self, request, pk, format=None):
        try:
            task = Task.objects.get(pk=pk) 
            task.delete()
            return Response({
                    'status': 'success',
                    'message': 'task deleted',
                })
        except Task.DoesNotExist:
            return Response('Not found', status=404)
        
class TaskAssignAdmin(APIView):
    permission_classes = (IsAuthenticated,AdminRequired)
    def post(self , request):
        taskID = request.data.get("taskID")
        assignee_Email = request.data.get("assignee_Email")
        user = MyUser.objects.get(email=assignee_Email)
        if TaskUser.objects.filter(taskID=taskID).exists():
            taskID = TaskUser.objects.filter(taskID=taskID)
            check_usermail = [item.assignee_Email for item in taskID]
            for x in check_usermail :
                if assignee_Email == x:
                    return Response("this task is already assign to this user")
        serializer = TaskUserSerializer(data=request.data)
        if serializer.is_valid():
            USER = request.user
            serializer.save(assignee_ID=user,assignee_username=user,assignor_ID=USER,assignor_username=USER)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self , request):
        user = request.user
        try:
            todo_task = TaskUser.objects.filter(assignor_ID=user)
            serializer = TaskUserSerializer(todo_task, many=True)
            return Response(serializer.data)
        except TaskUser.DoesNotExist:
            return Response('Not found', status=404)

class TaskAssignManager(APIView):
    permission_classes = (IsAuthenticated,ManagerRequired)
    def post(self , request):
        taskID = request.data.get("taskID")
        assignee_Email = request.data.get("assignee_Email")
        try:
            user = MyUser.objects.get(email=assignee_Email)
        except MyUser.DoesNotExist:
            return Response("assignee's mail not found", status=404)
            
        if TaskUser.objects.filter(taskID=taskID).exists():
            taskID = TaskUser.objects.filter(taskID=taskID)
            check_usermail = [item.assignee_Email for item in taskID]
            for x in check_usermail :
                if assignee_Email == x:
                    return Response("this task is already assign to this user")
        serializer = TaskUserSerializer(data=request.data)
        if serializer.is_valid():
            USER = request.user
            serializer.save(assignee_ID=user,assignee_username=user,assignor_ID=USER,assignor_username=USER)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self , request):
        user = request.user
        try:
            todo_task = TaskUser.objects.filter(assignor_ID=user)
            serializer = TaskUserSerializer(todo_task, many=True)
            return Response(serializer.data)
        except TaskUser.DoesNotExist:
            return Response('Not found', status=404)


#user can find their tasks #
class TaskAssignGet(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self , request ,format=None ):
        email = request.user.email
        users_task = TaskUser.objects.filter(assignee_Email=email)
        serializer = TaskUserSerializer(users_task, many=True)
        return Response(serializer.data)


class TaskInfo(APIView):
    def get(self, request, pk, format=None):
        log_task = Task.objects.get(pk=pk)
        serializer = TaskSerializer(log_task)
        return Response(serializer.data)


class BulkDeleteTask(APIView):
    permission_classes = (IsAuthenticated,AdminRequired)
    def post(self, request):
        delete_ids = request.data.get("delete_ids")
        Task.objects.filter(pk__in=delete_ids).delete()
        return Response("All task deleted")
        
class BulkAddTaskAdmin(APIView):
    permission_classes = (IsAuthenticated,AdminRequired)
    def post(self, request,):
        task= request.data.get("tasks")
        for i in task:
            serializer = TaskSerializer(data=i)
            if serializer.is_valid():
                user = request.user
                serializer.save(creator_ID=user,Creator_username=user)
            else:
                return Response("Task is already exist or Not valid ", status=400)
        return Response("Tasks Created Successfully")

class BulkAddTaskManager(APIView):
    permission_classes = (IsAuthenticated,ManagerRequired)
    def post(self, request,):
        task= request.data.get("tasks")
        for i in task:
            serializer = TaskSerializer(data=i)
            if serializer.is_valid():
                user = request.user
                serializer.save(creator_ID=user,Creator_username=user)
            else:
                return Response("Task is already exist or Not valid ", status=400)
        return Response("Tasks Created Successfully")
