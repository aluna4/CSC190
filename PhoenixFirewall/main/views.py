import os
import requests
import regex as re
import ipaddress
from dotenv import load_dotenv, find_dotenv
from django.http import HttpResponse
from .models import userlogIn
from .models import AddRule
from .models import DeleteRule
from .forms import SecurityConfUpload
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login



# Varibles for config
load_dotenv(find_dotenv())
USER=os.getenv('PHOENIX_USER')
PASS=os.getenv('PHOENIX_PASS')
URL=os.getenv('PAN_URL')
User = get_user_model()

def home(request):
    return render(request, 'homepage.html')

def add_success(request):
    return HttpResponse("Firewall Rule added successfully", status=200)
    
def delete_success(request):
    return HttpResponse("Firewall Rule deleted successfully", status=200)

def commit_success(request):
    return HttpResponse("Firewall Rule commited successfully", status=200)
    
def config_sucess_resp(request):
    return HttpResponse("Security Config Uploaded Successfully", status=200)


def create_user_view(request):
    if request.method == 'POST':
        # Get data from the form
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        employee_id = request.POST.get('employee_id')

        # Check if the username or employee ID already exists
        if userlogIn.objects.filter(username=username).exists():
             messages.error(request, "Username already exists")
             return render(request, 'create_user.html')
        if userlogIn.objects.filter(employeeID=employee_id).exists():
            messages.error(request, "Employee ID already exists")
            return render(request, 'create_user.html')
        
        # Create the user
        try:
            User.objects.create_user( #userlogIn(
                username=username,
                password=password,#make_password(password),
                first_name=first_name.upper(),
                last_name=last_name.upper(),
                employeeID=employee_id
            )
            #new_user.save()
            messages.success(request, "User created successfully. Please log in.")
            return redirect('login')
        except ValidationError as e:
            # Handle validation errors from the model here
            for field, errors in e.message_dict.items():
                for error in errors:
                    messages.error(request, error)
            return render(request, 'create_user.html')
    else:
        return render(request, 'create_user.html')

#log in page
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            # Get the userlogIn object with the given username
            user = authenticate(request, username=username, password=password)#userlogIn.objects.get(user_name=username)
            
            if user is not None:
                login(request,user)
                if user.is_superuser:
                    return redirect('admin')
                else:
                    return redirect('user')
            else:
                messages.error(request, 'Invalid username or password')
        except: 
                messages.error(request, 'User does not exist')
    return render(request, 'login.html')

#user page
def user_view(request):
    context = {
        'username': request.user
    }
    return render(request, 'user.html', context)

# admin page
def admin_view(request):
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

        
        # Check if the flow is allowed
        if (source_zone, destination_zone) not in ALLOWED_FLOWS:
            messages.error(request,'The specified flow is not allowed.')
            return render(request, "add_rule.html")

        # Validate IP addresses
        if source_zone in ZONE_SUBNETS and destination_zone in ZONE_SUBNETS:
            source_ip_valid = ipaddress.ip_address(source_ip) in ZONE_SUBNETS [source_zone]
            destination_ip_valid = ipaddress.ip_address(destination_ip) in ZONE_SUBNETS[destination_zone]

            if not source_ip_valid or not destination_ip_valid:
                messages.error(request, 'The IP address entered is not within the correct zone.')
                return render(request, "add_rule.html")

        current_user = get_object_or_404(userlogIn, pk=request.user.pk)

        new_rule = Rule(
            employeeID = current_user,
            rule_name = rule_name.upper(),
            source_zone = source_zone, 
            source_ip = source_ip, 
            destination_zone = destination_zone,
            destination_ip = destination_ip,
            application = application,
            service = service,
            action = action
        )
        new_rule.save()
        messages.success(request, "Rule created successfully")
        return redirect('user')
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
            #call panorama_api function
            success = delete_firewall_rule(context['rule_name'], context['source_ip'], context['port'])
            if success:
                return render(request, "delete_rule.html", {'success': 'Rule deleted successfully.'})
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
            #call panorama_api function
            success = commit_firewall_rule(context['rule_name'], context['destination_zone'], context['port'])
            if success:
                return render(request, "commit_rule.html", {'success': 'Configurations committed successfully.'})
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


# Handle upload file
def handle_uploaded_file(f):
    with open("/tmp/upl_security_config.txt", "wb+") as destination:
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
def _set_pan_security_config(request, file):
    # Gemerate API key
    key = _get_api_key(request)

    # upload config rules via API
    headers = {"X-PAN-KEY":key}
    requests.post(f"{URL}/api/?type=config&action=set&xpath=/config/devices/entry/vsys/entry/rulebase/security/rules/entry[@name='vsys1']&element={file}", headers=headers, verify=False)
    
# Function used to handle file uploads from upload template
def upload(request):  
    if request.method == 'POST':  
        file = SecurityConfUpload(request.POST, request.FILES)  
        if file.is_valid():  
            handle_uploaded_file(request.FILES['file'])

            # This requires further testing to get the xml correct
            # _set_pan_security_config(request, request.FILES['/tmp/upl_security_config.txt'])  
            return HttpResponse("File uploaded successfuly")  
    else:  
        upload = SecurityConfUpload()  
        return render(request,"upload.html",{'form':upload})  
