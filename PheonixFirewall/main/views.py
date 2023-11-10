from django.http import HttpResponse
from django.shortcuts import render, redirect
from .panorama_api import add_firewall_rule
from django.contrib.auth import authenticate, login

def home(request):
    return HttpResponse("Phoenix Firewall Homepage", status=200)

#log in page
def log_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # User authentication successful, log the user in
            login(request, user)
            return render(request, "AddRule.html")  # Redirect to the add rule page after login
        else:
            # Authentication failed, handle the error (display an error message, redirect to login page, etc.)
            error_message = "Invalid username or password. Please try again."
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, "login.html")
    

# add firewall rule
def add_rule(request):
    if request.method == "POST":
        rule_name = request.POST.get("rule_name")
        ip = request.POST.get("ip")
        port = request.POST.get("port")
        
        # call panorama_api function
        add_firewall_rule(rule_name, ip, port)

        # redirect back to home page
        return redirect('home')  
    else:
        # if not POST then for now just show addrule.html
        return render(request, "AddRule.html")
