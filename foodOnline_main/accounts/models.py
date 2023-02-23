from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self,email,first_name,last_name,username,password=None):
        if not email:
            raise ValueError("User must Provide Email")
        if not username:
            raise ValueError("User must Provide username")
        
        user =self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            username = username
        )
        user.set_password(password)
        user.save(using= self._db)
        return user


    def create_superuser(self,email,first_name,last_name,username,password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )

        user.is_admin = True,
        user.is_active = True,
        user.is_staff = True,
        user.is_Superadmin = True,
        user.save(using=self._db)
        return user

       

class User(AbstractBaseUser):
    Restaurant = 1
    customer = 2

    ROLE_CHOICES = (
        (Restaurant,'restare'),
        (customer,'customer')
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50,unique=True)
    email = models.EmailField(max_length=100,unique=True)
    phonenumber = models.CharField(max_length=12,blank=True)
    role =  models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)


    #required fileds
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin= models.BooleanField(default=False)


    objects = UserManager()


    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    def __str__(self):
        return self.email


    def has_perm(self):
        return self.is_admin
    
    def has_module_perms(self,app_label):
        return True 
