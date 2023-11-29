from django.http import HttpResponse
from django.shortcuts import render, redirect
from .panorama_api import add_firewall_rule
from django.contrib.auth import authenticate, login
from django.contrib import messages

def index(request):
    return HttpResponse("OK - Home", status=200)

# add firewall rule
def add_rule(request):
    if request.method == "POST":
        rule_name = request.POST.get("rule_name")
        ip = request.POST.get("ip")
        port = request.POST.get("port")
        
        # call panorama_api function
        add_firewall_rule(rule_name, ip, port)

        # redirect back to home page
        return redirect('index')  
    else:
        # if not POST then for now just show addrule.html
        return render(request, "AddRule.html")

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, "User.html")
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')