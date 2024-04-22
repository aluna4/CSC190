import os
import requests
import regex as re
import ipaddress
from dotenv import load_dotenv, find_dotenv
from django.http import HttpResponse
from .models import userlogIn
from .models import Rule
from .forms import SecurityConfUpload
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from .panorama_api import add_firewall_rule
from .panorama_api import delete_firewall_rule


# variables for config
load_dotenv(find_dotenv())
USER=os.getenv('PHOENIX_USER')
PASS=os.getenv('PHOENIX_PASS')
URL=os.getenv('PAN_URL')
User = get_user_model()

def home(request):
    # render the homepage.html template
    return render(request, 'homepage.html')

def add_success(request):
    # return a success response for adding a firewall rule
    return HttpResponse("Firewall Rule added successfully", status=200)
    
def delete_success(request):
    # return a success response for deleting a firewall rule
    return HttpResponse("Firewall Rule deleted successfully", status=200)

def commit_success(request):
    # return a success response for committing a firewall rule
    return HttpResponse("Firewall Rule committed successfully", status=200)
    
def config_sucess_resp(request):
    # return a success response for uploading a security config
    return HttpResponse("Security Config Uploaded Successfully", status=200)


def create_user_view(request):
    if request.method == 'POST':
        # get data from the form
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        employee_id = request.POST.get('employee_id')

        # check if the username or employee ID already exists
        if userlogIn.objects.filter(username=username).exists():
             messages.error(request, "Username already exists")
             return render(request, 'create_user.html')
        if userlogIn.objects.filter(employeeID=employee_id).exists():
            messages.error(request, "Employee ID already exists")
            return render(request, 'create_user.html')
        if username.lower() in password.lower():
            messages.error(request, "Password cannot be similar to username")
            return render(request, 'create_user.html')
        
        # create the user
        try:
            User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name.upper(),
                last_name=last_name.upper(),
                employeeID=employee_id
            )
            messages.success(request, "User created successfully. Please log in.")
            return redirect('login')
        except ValidationError as e:
            # handle validation errors from the model here
            for field, errors in e.message_dict.items():
                for error in errors:
                    messages.error(request, error)
            return render(request, 'create_user.html')
    else:
        return render(request, 'create_user.html')

# log in page
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            # get the user object with the given username
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request,user)
                if user.is_superuser:
                    return redirect('custom_admin')
                else:
                    return redirect('user')
            else:
                messages.error(request, 'Invalid username or password')
        except: 
                messages.error(request, 'User does not exist')
    return render(request, 'login.html')

# user page
@login_required
def user_view(request):
    context = {
        'username': request.user
    }
    return render(request, 'user.html', context)

# admin page
@login_required
@user_passes_test(lambda u: u.is_superuser)
def custom_admin_view(request):
    context = {
        'username': request.user
    }
    return render(request, 'admin.html', context)

# define allowed flows based on the simulated subnet segmentation
ALLOWED_FLOWS = [
    ('Internal', 'DMZ'),
    ('Internal', 'Internet'),
    ('Internet', 'DMZ')
]

# define zone to subnet mappings
ZONE_SUBNETS = {
    'Internal': ipaddress.ip_network('10.0.0.0/26'),
    'DMZ': ipaddress.ip_network('10.0.0.64/26'),
    'Internet': ipaddress.ip_network('10.0.0.128/26'),
    'Other': ipaddress.ip_network('10.0.0.192/26'),
}

# add firewall rule
def add_rule(request):
    if request.method == "POST":
        rule_name = request.POST.get("rule_name")
        source_zone = request.POST.get("source_zone")
        source_ip = request.POST.get("source_ip")
        destination_zone = request.POST.get("destination_zone")
        destination_ip = request.POST.get("destination_ip")
        application = request.POST.get("application")
        service = request.POST.get("service")
        action = request.POST.get("action")

        current_user = request.user

        # check if the flow is allowed
        user_zones = current_user.zones
        if source_zone not in user_zones or destination_zone not in user_zones:
            messages.error(request,'The specified flow is not allowed. You do not have access to a zone')
            return render(request, "add_rule.html")

        # validate IP addresses
        if source_zone in ZONE_SUBNETS and destination_zone in ZONE_SUBNETS:
            source_ip_valid = ipaddress.ip_address(source_ip) in ZONE_SUBNETS [source_zone]
            destination_ip_valid = ipaddress.ip_address(destination_ip) in ZONE_SUBNETS[destination_zone]

            if not source_ip_valid or not destination_ip_valid:
                messages.error(request, 'The IP address entered is not within the correct zone.')
                return render(request, "add_rule.html")

        # prepare data for api call
        api_data = {
            'rule_name': rule_name,
            'source_ip': source_ip,
            'destination_ip': destination_ip,
            'application': application,
            'service': service,
            'action': action,
            'source_zone': source_zone,
            'destination_zone': destination_zone
        }

        try:
            # call panorama_api function to add the firewall rule
            success = add_firewall_rule(rule_name=rule_name, source_zone=source_zone, source_ip=source_ip,
                                        destination_zone=destination_zone, destination_ip=destination_ip,
                                        application=application, service=service, action=action)
            if success:
                # add rule to database
                new_rule = Rule(
                    employeeID=current_user,
                    rule_name=rule_name.upper(),
                    source_zone=source_zone,
                    source_ip=source_ip,
                    destination_zone=destination_zone,
                    destination_ip=destination_ip,
                    application=application,
                    service=service,
                    action=action
                )
                new_rule.save()
                messages.success(request, "Rule created successfully")
                if request.user.is_superuser:
                    return redirect('custom_admin')
                else:
                    return redirect('user')
            else:
                messages.error(request, 'Failed to add firewall rule via API.')
                return render(request, "add_rule.html")
        except Exception as e:
            messages.error(request, f'Error adding firewall rule: {str(e)}')
            return render(request, "add_rule.html")
    else:
        return render(request, "add_rule.html")
        
# delete firewall rule
def delete_rule(request):
    context = {
        'username': request.user, 
        'rule_name': '',
        'source_ip':'',
        'port': '',
    }
    if request.method == "POST":
        context['rule_name'] = request.POST.get("rule_name")
        context['source_ip'] = request.POST.get("ip")
        context['port'] = request.POST.get("port")


        try:
            # call panorama_api function
            success = delete_firewall_rule(context['rule_name'], context['source_ip'], context['port'])
            if success:
                if request.user.is_superuser:
                    return render(request, "admin.html", {'success': 'Rule deleted successfully.'})
                else:
                    return render(request, "user.html", {'success': 'Rule deleted successfully.'})
            else:
                context['error'] = 'Error deleting firewall rule'
                return render(request, "delete_rule.html", context)
        except Exception as e:
            context['error'] = str(e)
            return render(request, "delete_rule.html", context)
    else:
        # if not POST then for now just show addrule.html
        return render(request, "delete_rule.html", context)

def commit_rule(request):
    context = {
        'username': request.user,
        'rule_name': '',
        'destination_zone': '',
        'port': '',
    }
    if request.method == "POST":
        context['rule_name'] = request.POST.get("rule_name")
        context['destination_zone'] = request.POST.get('destination_zone')
        context['port'] = request.POST.get("port")

        try:
            # call panorama_api function
            success = commit_firewall_rule(context['rule_name'], context['destination_zone'], context['port'])
            if success:
                if request.user.is_superuser:
                    return render(request, "admin.html", {'success': 'Rule committed successfully.'})
                else:
                    return render(request, "user.html", {'success': 'Rule committed successfully.'})
            else:
                context['error'] = 'Error committing configurations'
                return render(request, "commit_rule.html", context)
        except Exception as e:
            context['error'] = str(e)
            print(context['error'])
            return render(request, "commit_rule.html", context)
    else:
        # if not POST then for now just show addrule.html
        return render(request, "commit_rule.html", context)


# handle upload file
def handle_uploaded_file(f):
    with open("/tmp/upl_security_config.txt", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def _get_api_key(request):
    # send POST request to get headers form 
    headers = {"Content-Type":"application/x-www-form-urlencoded"}
    data = {"user":f"{USER}", "password":f"{PASS}"}
    r = requests.post(f"{URL}api/?type=keygen", data=data, headers=headers, verify=False)

    # parse key with regex
    key = re.search("<key>(\w+==)<", r.text)

    # return key from function
    return(key.group(1))


# function to get Django to download the file
def _download_config(request):
    file_path = '/tmp/security_policies.txt'
    # open the file in binary mode
    with open(file_path, 'r') as file:
        # set the content type to the appropriate file type (text/plain for .txt files)
        response = HttpResponse(file, content_type='text/plain')
        # set the Content-Disposition header to attach the file as a download
        response['Content-Disposition'] = 'attachment; filename="security_policies.txt"'
        return response

# function to grab config from PAN
def get_pan_security_config(request):
    # generate API key for authentication
    key = _get_api_key(request)

    # pull config file
    headers = {"X-PAN-KEY":key}
    security_policies = requests.post(f"{URL}/api?type=config&action=get&xpath=/config/devices/entry/vsys/entry[@name='vsys1']&key={key}", headers=headers, verify=False)

    # write config file to /tmp/ 
    with open('/tmp/security_policies.txt', 'w') as config_file:
        config_file.write(security_policies.text)

    # download config
    return (_download_config(request))

    # delete config off server
    #time.sleep(3)
    #os.remove("/tmp/firewall-config.xml")

# function to set security config rules on PAN
# note, this will change the default rulesets
# documentation for API: https://docs.paloaltonetworks.com/pan-os/9-1/pan-os-panorama-api/pan-os-xml-api-request-types/configuration-api/set-configuration#id52c0a29e-5573-4a40-bccf-5585fee352f3
def _set_pan_security_config(request, file):
    # generate API key
    key = _get_api_key(request)

    # upload config rules via API
    headers = {"X-PAN-KEY":key}
    requests.post(f"{URL}/api/?type=config&action=set&xpath=/config/devices/entry/vsys/entry/rulebase/security/rules/entry[@name='vsys1']&element={file}", headers=headers, verify=False)
    
# function used to handle file uploads from upload template
def upload(request):  
    if request.method == 'POST':  
        file = SecurityConfUpload(request.POST, request.FILES)  
        if file.is_valid():  
            handle_uploaded_file(request.FILES['file'])

            # this requires further testing to get the xml correct
            # _set_pan_security_config(request, request.FILES['/tmp/upl_security_config.txt'])  
            return HttpResponse("File uploaded successfully")  
    else:  
        upload = SecurityConfUpload()  
        return render(request,"upload.html",{'form':upload})
