from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class userlogInManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given username and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        """
        Creates and saves a superuser with the given username and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

# Create your models here. This is where the db gets created.
class userlogIn(AbstractBaseUser, PermissionsMixin):
   first_name = models.CharField(max_length = 15, default = "emp_FirstName") #holds employee first name
   last_name = models.CharField(max_length = 15, default = "emp_LastName") #holds employee last name
   username = models.CharField(max_length=100,unique=True) #holds username
   password = models.CharField(max_length=250) #holds user password
   employeeID = models.CharField(max_length=8,unique=True,validators=[RegexValidator(regex=r'^\d{8}$')]) #holds employee 8 digit ID number
   create_date = models.DateTimeField("date created",auto_now_add=True) #holds date of user created
   zones = models.JSONField(default=list)
   is_staff = models.BooleanField(default=False)
   is_superuser = models.BooleanField(default=False)
   is_active = models.BooleanField(default=True)  # Added is_active field

   objects = userlogInManager()

   USERNAME_FIELD = 'username'
   REQUIRED_FIELDS = ['first_name', 'last_name', 'employeeID']

   def clean(self):
      # Check that the password is at least 8 characters
      if len(self.password) < 8:
         raise ValidationError({'password': "Password must be at least 8 characters long"})

      # Check that the password is not similar to the user_name
      if self.password.lower() in self.username.lower():
         raise ValidationError({'password': "Password can not be the same as the username"})
   
   #Overrides save method to go through the validate method first
   def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
   
   def __str__(self):
      return f"Employee: {self.employeeID}, Username = {self.username}"

class Rule(models.Model):
   employeeID = models.ForeignKey(userlogIn, on_delete=models.CASCADE)
   rule_name = models.CharField(max_length=50)
   source_zone = models.CharField(max_length=50)
   source_ip = models.CharField(max_length=50)
   destination_zone = models.CharField(max_length=50)
   destination_ip = models.CharField(max_length=50)
   application = models.CharField(max_length=50)
   service = models.CharField(max_length=50)
   action = models.CharField(max_length=50)
   def __str__(self):
      return f"Employee: {self.employeeID.employeeID} Rule Name = {self.rule_name}"