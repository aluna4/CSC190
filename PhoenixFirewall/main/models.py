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

   def __str__(self):
      return "Employee: "+self.employeeID+", Username = "+self.user_name
   
   def was_created_recently(self):
      return self.create_date >= timezone.now() - datetime.timedelta(days=1)

   class Meta:
      constraints = [models.UniqueConstraint(fields=['user_name'], name='unique_user_name')]
      constraints = [models.UniqueConstraint(fields=['employeeID'], name='unique_employeeID')]

class scripts(models.Model):
   employeeID = models.CharField(max_length=10) #holds employee ID number
   scriptTxt = models.CharField(max_length=100) #holds script created by user

   def __str__(self):
      return "Employee: " +self.employeeID+ ", Script = "+self.scriptTxt
   
   def save(self, *args, **kwargs):
        # Check if employeeID exists in the userlogIn table
        if not userlogIn.objects.filter(employeeID=self.employeeID).exists():
            raise ValidationError(f"Employee ID {self.employeeID} does not exist in the database.")
        super(scripts, self).save(*args, **kwargs)