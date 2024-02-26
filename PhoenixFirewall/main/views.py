import os
import time
import datetime
import requests
import regex as re
from dotenv import load_dotenv, find_dotenv
from django.http import HttpResponse, Http404
from django.contrib.auth.hashers import make_password
from .models import userlogIn

from django.contrib import messages
from django.http import HttpResponse
from .panorama_api import add_firewall_rule
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponseBadRequest

# Varibles for config
load_dotenv(find_dotenv())
USER=os.getenv('PHOENIX_USER')
PASS=os.getenv('PHOENIX_PASS')
URL=os.getenv('PAN_URL')

def home(request):
    return render(request, 'homepage.html')

def create_user_view(request):
    return render(request, 'create_user.html')

def add_success(request):
    return HttpResponse("Firewall Rule added successfully", status=200)
    
def delete_success(request):
    return HttpResponse("Firewall Rule deleted successfully", status=200)

def config_sucess_resp(request):
    return HttpResponse("Security Config Uploaded Successfully", status=200)


def create_user(request):
    if request.method == 'POST':
        # Get data from the form
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        employee_id = request.POST.get('employee_id')

        # Check if the username or employee ID already exists
        if userlogIn.objects.filter(user_name=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'create_user.html')
        if userlogIn.objects.filter(employeeID=employee_id).exists():
            messages.error(request, "Employee ID already exists.")
            return render(request, 'create_user.html')

        # Create the user
        new_user = userlogIn(
            first_name=first_name,
            last_name=last_name,
            user_name=username,
            user_pswd=make_password(password),  # Hash the password
            employeeID=employee_id,
            create_date=datetime.timezone.now()
        )
        new_user.save()
        
        # Redirect to the login page after creating the user
        messages.success(request, "User created successfully. Please log in.")
        return redirect('login')  # Replace 'login' with the name of your login URL
    else:
        # If not a POST request, render the form again
        return render(request, 'create_user.html')
    


#log in page
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'User.html')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

#user page
def user_view(request):
    return render(request, 'User.html')

# define allowed flows based on the simulated subnet segmentation
ALLOWED_FLOWS = [
    ('Internal', 'DMZ'),
    ('Internal', 'Internet'),
]

# add firewall rule
def add_rule(request):
    context = {
        'rule_name': '',
        'source_zone': '',
        'source_ip': '',
        'destination_zone': '',
        'destination_ip': '',
        'application': '',
        'service': '',
        'action': 'allow',
        'error': '',
    }

    if request.method == "POST":
        context['rule_name'] = request.POST.get("rule_name")
        context['source_zone'] = request.POST.get("source_zone")
        context['source_ip'] = request.POST.get("source_ip")
        context['destination_zone'] = request.POST.get("destination_zone")
        context['destination_ip'] = request.POST.get("destination_ip")
        context['application'] = request.POST.get("application")
        context['service'] = request.POST.get("service")
        context['action'] = request.POST.get("action")
        
        # Check if the flow is allowed
        if (context['source_zone'], context['destination_zone']) not in ALLOWED_FLOWS:
            context['error'] = 'The specified flow is not allowed.'
            return render(request, "AddRule.html", context)

        try:
            success = add_firewall_rule(context['rule_name'], context['source_zone'], context['source_ip'], context['destination_zone'], context['destination_ip'], context['application'], context['service'], context['action'])
            if success:
                return render(request, "AddRule.html", {'success': 'Rule added successfully.'})
            else:
                context['error'] = 'Error adding firewall rule'
                return render(request, "AddRule.html", context)
        except Exception as e:
            context['error'] = str(e)
            return render(request, "AddRule.html", context)
    else:
        return render(request, "AddRule.html")
# delete firewall rule
def delete_rule(request):
    if request.method == "POST":
        rule_name = request.POST.get("rule_name")
        ip = request.POST.get("ip")
        port = request.POST.get("port")

        # call panorama_api function
        # delete_firewall_rule(rule_name, ip, port)

        # redirect back to home page
        return redirect('delete_success')
    else:
        # if not POST then for now just show addrule.html
        return render(request, "DeleteRule.html")
    
# Handle upload file
def handle_uploaded_file(f):
    with open("tmp/security_config.txt", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def _get_api_key(request):
    # Send POST request to get headers form 
    headers = {"Content-Type":"application/x-www-form-urlencoded"}
    data = {"user":f"{USER}", "password":f"{PASS}"}
    r = requests.post(f"{URL}api/?type=keygen", data=data, headers=headers, verify=False)

    # Parse key with regex
    key = re.search("<key>(\w+==)<", r.text)

    # Return key from function
    return(key.group(1))


# Function to get Django to download the file
def _download_config(request):
    file_path = '/tmp/security_policies.txt'
    # Open the file in binary mode
    with open(file_path, 'r') as file:
        # Set the content type to the appropriate file type (text/plain for .txt files)
        response = HttpResponse(file, content_type='text/plain')
        # Set the Content-Disposition header to attach the file as a download
        response['Content-Disposition'] = 'attachment; filename="security_policies.txt"'
        return response

# Function to read security config from upload form 
def _read_config(request):
    if request.method == 'POST':
        file = request.FILES['security_config']

        if file.size > 2000000:
            return HttpResponseBadRequest()
        return file

# Function to grab config from PAN
def get_pan_security_config(request):
    # Generate API key for authentication
    key = _get_api_key(request)

    # Pull config file
    headers = {"X-PAN-KEY":key}
    security_policies = requests.post(f"{URL}/api?type=config&action=get&xpath=/config/devices/entry/vsys/entry[@name='vsys1']&key={key}", headers=headers, verify=False)

    # Write config file to /tmp/ 
    with open('/tmp/security_policies.txt', 'w') as config_file:
        config_file.write(security_policies.text)

    # Download config
    return (_download_config(request))

    # Delete config off server
    #time.sleep(3)
    #os.remove("/tmp/firewall-config.xml")

# Function to set security config rules on PAN
# Note, this will change the default rulesets
# Documentation for API: https://docs.paloaltonetworks.com/pan-os/9-1/pan-os-panorama-api/pan-os-xml-api-request-types/configuration-api/set-configuration#id52c0a29e-5573-4a40-bccf-5585fee352f3
def set_pan_security_config(request):
    try:
        # Gemerate API key
        key = _get_api_key(request)

        # Load security config into memory
        file = _read_config(request)

        # upload config rules via API
        headers = {"X-PAN-KEY":key}
        requests.post(f"{URL}/api/?type=config&action=set&xpath=/config/devices/entry/vsys/entry/rulebase/security/rules/entry[@name='vsys1']&element={file}", headers=headers, verify=False)
        return render(request, config_sucess_resp(request))
    except:
        return HttpResponseBadRequest()
    