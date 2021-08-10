from django.db import models
from datetime import datetime
from django.utils import timezone
from Accounts.models import MyUser
# Create your models here.
class Task(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    Creator_username = models.CharField(max_length=100, null = True,default="", blank=False)
    creator_ID = models.ForeignKey(MyUser,related_name='Created', on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField()
    def __str__(self , request):
        return self.user.username
    
class TaskUser(models.Model):
    taskID= models.CharField(max_length=100, blank=False)
    assignor_username= models.CharField(max_length=100, null=True,blank=True)
    assignee_username= models.CharField(max_length=100,null=True,blank=True)
    assignee_Email =  models.EmailField(max_length=254, null=False, blank=False)
    assignor_ID = models.ForeignKey(MyUser,related_name='Assign_by',null=True,blank=True, on_delete=models.CASCADE)
    assignee_ID = models.ForeignKey(MyUser, related_name='Assign_for',null=True,blank=True,on_delete=models.CASCADE)
    description = models.TextField()
    
    def __str__(self):
        return self.title
    