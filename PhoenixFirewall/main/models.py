import datetime

from django.db import models
from django.utils import timezone

# Create your models here. This is where the db gets created.
class userlogIn(models.Model):
   user_name = models.CharField(max_length=100) #holds username
   user_pswd = models.CharField(max_length=50) #holds user password
   employeeID = models.CharField(max_length=10) #holds employee ID number
   create_date = models.DateTimeField("date created") #holds date of user created

   def __str__(self):
      return "Employee: "+self.employeeID+", Username = "+self.user_name
   
   def was_created_recently(self):
      return self.create_date >= timezone.now() - datetime.timedelta(days=1)

class scripts(models.Model):
   employeeID = models.CharField(max_length=10) #holds employee ID number
   scriptTxt = models.CharField(max_length=100) #holds script created by user

   def __str__(self):
      return "Employee: "+self.employeeID+ ", Script = "+self.scriptTxt