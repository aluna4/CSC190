import os
import time
import datetime
import requests
from dotenv import load_dotenv, find_dotenv
from django.http import HttpResponse, Http404

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
      return "Employee: " +self.employeeID+ ", Script = "+self.scriptTxt
   
# Class for pan config
class pan_collector(models.Model):
   # Varibles for config
   load_dotenv(find_dotenv())
   USER=os.getenv('PHOENIX_USER')
   PASS=os.getenv('PHOENIX_PASS')
   URL=os.getenv('PAN_URL')

   # Function to get Django to download the file
   def download_config(self):
    file_path = '/tmp/firewall-config.xml'
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="text/html")
            response['Content-Disposition'] = 'inline; filename=' + file_path
            return response
    raise Http404

   # Function to grab config from PAN
   def get_pan_config(self):
      # Generate API key for authentication
      key = f"{self.URL}/api/?type=keygen&user={self.USER}&password={self.PASS}"
      response = requests.get(key, verify=False) 
      api_key = response.xml.find('.//key').text

      # Pull config file
      config_url = f"{self.URL}/api/?type=export&category=configuration&key={api_key}"
      config_response = requests.get(config_url, verify=False)

      # Write config file to /tmp/ 
      with open('/tmp/firewall-config.xml', 'w') as config_file:
         config_file.write(config_response.text)

      # Download config
      self.download_config()

      # Delete config off server
      time.sleep(3)
      os.remove("/tmp/firewall-config.xml")