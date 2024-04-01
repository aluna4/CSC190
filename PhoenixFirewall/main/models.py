from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here. This is where the db gets created.
class userlogIn(models.Model):
   first_name = models.CharField(max_length = 15) #holds employee first name
   last_name = models.CharField(max_length = 15) #holds employee last name
   user_name = models.CharField(max_length=100) #holds username
   user_pswd = models.CharField(max_length=50) #holds user password
   employeeID = models.CharField(max_length=10) #holds employee ID number
   create_date = models.DateTimeField("date created") #holds date of user created
   zones = models.JSONField(default=list)

   def get_employeeID(self):
      return self.employeeID
   
   def __str__(self):
      return f"Employee: {self.employeeID}, Username = {self.user_name}"
   
   # def was_created_recently(self):
   #    return self.create_date >= timezone.now() - datetime.timedelta(days=1)

   class Meta:
      constraints = [models.UniqueConstraint(fields=['user_name'], name='unique_user_name')]
      constraints = [models.UniqueConstraint(fields=['employeeID'], name='unique_employeeID')]

class Rule(models.Model):
   employeeID = models.CharField(max_length=10)
   rule_name = models.CharField(max_length=50)
   source_zone = models.CharField(max_length=50)
   source_ip = models.CharField(max_length=50)
   destination_zone = models.CharField(max_length=50)
   destination_ip = models.CharField(max_length=50)
   application = models.CharField(max_length=50)
   service = models.CharField(max_length=50)
   action = models.CharField(max_length=50)   

   def __str__(self):
      return f"Employee: {self.employeeID} Rule Name = {self.rule_name}"
   
class Zones(models.Model):
   zone_name = models.CharField(max_length=15)
   start_zone = models.CharField(max_length=50)
   end_zone = models.CharField(max_length=50)
   source_ip = models.CharField(max_length=50)
   destination_ip = models.CharField(max_length=50)
   source_zone = models.CharField(max_length=50)
   destination_zone = models.CharField(max_length=50)

   def __str__(self):
      return f"Zone: {self.zone_name}"
   

      
