from rest_framework.routers import DefaultRouter
from django.urls import path, include, re_path as url
from Usertask.views import TaskDetailManager,TaskDetailAdmin ,AllTaskListAdmin,AllAssignTaskListAdmin, TaskListAdmin, TaskListManager, TaskAssignAdmin ,BulkAddTaskAdmin,BulkAddTaskManager,TaskAssignManager,TaskAssignGet , TaskInfo,BulkDeleteTask

urlpatterns = [

    url(r'^task_admin/$', TaskListAdmin.as_view()),
    url(r'^all_task_admin/$', AllTaskListAdmin.as_view()),
    url(r'^all_assigntask_admin/$', AllAssignTaskListAdmin.as_view()),
    url(r'^task_manager/$', TaskListManager.as_view()),
    url(r'^TaskAssignAdmin/$', TaskAssignAdmin.as_view()),
    url(r'^TaskAssignManager/$', TaskAssignManager.as_view()),
    url(r'^taskAssignGet/$', TaskAssignGet.as_view()),
    url(r'^BulkAddTaskAdmin/$', BulkAddTaskAdmin.as_view()),
    url(r'^BulkAddTaskManager/$', BulkAddTaskManager.as_view()),
    url(r'^BulkDeleteTask/$', BulkDeleteTask.as_view()),
    path('taskviewManager/<int:pk>/', TaskDetailManager.as_view()),
    path('taskviewAdmin/<int:pk>/', TaskDetailAdmin.as_view()),
    path('taskInfo/<int:pk>/', TaskInfo.as_view()),
]