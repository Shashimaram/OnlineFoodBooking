from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,first_name, last_name, username, email,password=None):
        if not email:
            raise ValueError("user must have an email address")
    
        if not user_name:
            raise ValueError("user must have a username")
    
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self,first_name, last_name, username, email,password=None):
        user=self.create_superuser(
            email= self.normalize_email(email),
            username = username,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using = self._db)
        return user

class User(AbstractBaseUser):
    RESTAURANT = 1
    CUSTOMER = 2
    ROLE_CHOICES = (
        (RESTAURANT,'Restaurant'),
        (CUSTOMER,'Customer'),
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    usernamae= models.CharField(max_length=50, unique= True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=100, unique=True)
    roles = models.PositiveSmallIntegerField(choices=ROLE_CHOICES,blank=True, null=True)

    # required fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now = True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'firstname','lastname',]

    def __str__(self) -> str:
        return self.email 

    def has_perm(self, perm, obj = None):
        return self.is_admin

    def has_module_perms(self, app_lable):
        return True


# class mymodel(models.Model):
# text = models.CharField(max_length=199)
# name = models.CharField(max_length=200)