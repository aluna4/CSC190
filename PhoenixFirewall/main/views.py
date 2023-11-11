from django.http import HttpResponse
from django.shortcuts import render, redirect
from .panorama_api import add_firewall_rule


def home(request):
    return HttpResponse("Phoenix Firewall Homepage", status=200)

#log in page
def log_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        #need to change the authentication method when log in 
        #after database is created
        #this is for demonstration only
        hardcoded_users = {
            'user1': 'user1pas',
            'user2': 'user2pas',
        }
        
        hardcoded_admins = {
            'admin': 'adminpass',
        }

        if username in hardcoded_users and password == hardcoded_users[username]:
            # User authentication successful
            request.session['logged_in_user'] = username
            return render(request, "AddRule.html")  # Redirect to the add rule page after login
        if username in hardcoded_admins and password == hardcoded_admins[username]:
            request.session['logged_in_user'] = username
            return render(request, "Admin.html")
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
