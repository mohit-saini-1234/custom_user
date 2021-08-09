from rest_framework.routers import DefaultRouter
from django.urls import path, include, re_path as url
from Usertask.views import TaskDetail , TaskList , TaskAssignAdmin ,BulkAddTask,TaskAssignManager,TaskAssignGet , TaskInfo,BulkDeleteTask

urlpatterns = [

    url(r'^task/$', TaskList.as_view()),
    url(r'^TaskAssignAdmin/$', TaskAssignAdmin.as_view()),
    url(r'^TaskAssignManager/$', TaskAssignManager.as_view()),
    url(r'^taskAssignGet/$', TaskAssignGet.as_view()),
    url(r'^BulkAddTask/$', BulkAddTask.as_view()),
    url(r'^BulkDeleteTask/$', BulkDeleteTask.as_view()),
    path('taskview/<int:pk>/', TaskDetail.as_view()),
    path('taskInfo/<int:pk>/', TaskInfo.as_view()),
]