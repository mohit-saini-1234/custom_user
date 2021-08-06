from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
    
class MyUserManager(BaseUserManager):
    def create_user(self, email, username,role,first_name, last_name, phone_number,address, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            role=role,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            address=address,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
# Create your models here.
class MyUser(AbstractBaseUser):
    role = models.CharField(max_length=20, blank=True, default='user' )
    email = models.EmailField(max_length=40, unique=True , error_messages={'unique':"This email has already been registered."})
    username = models.CharField(max_length=40, unique=True)
    first_name = models.CharField(max_length=40, )
    last_name = models.CharField(max_length=40, )
    password = models.CharField(max_length=40, )
    phone_number = models.IntegerField(max_length=10, unique=True)
    address = models.CharField(max_length=40, )
    objects = MyUserManager()
    REQUIRED_FIELDS = ['__all__']

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    
    