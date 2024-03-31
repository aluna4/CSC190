from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

# Create your models here. This is where the db gets created.
class userlogIn(models.Model):
   first_name = models.CharField(max_length = 15) #holds employee first name
   last_name = models.CharField(max_length = 15) #holds employee last name
   user_name = models.CharField(max_length=100,unique=True) #holds username
   user_pswd = models.CharField(max_length=50) #holds user password
   employeeID = models.CharField(max_length=8,unique=True,validators=[RegexValidator(regex=r'^\d{8}$')]) #holds employee 8 digit ID number
   create_date = models.DateTimeField("date created") #holds date of user created
   zones = models.JSONField(default=list)

   def clean(self):
      # Check that the password is at least 8 characters
      if len(self.user_pswd) < 8:
         raise ValidationError({'user_pswd': "Password must be at least 8 characters long."})

      # Check that the password is not similar to the user_name
      if self.user_pswd.lower() == self.user_name.lower():
         raise ValidationError({'user_pswd': "Password can not be the same as the username."})
   
   #Overrides save method to go through the validate method first
   def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

   def get_employeeID(self):
      return self.employeeID
   
   def __str__(self):
      return f"Employee: {self.employeeID}, Username = {self.user_name}"

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
