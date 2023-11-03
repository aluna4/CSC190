from django.http import HttpResponse
from django.shortcuts import render, redirect
from .panorama_api import add_firewall_rule

def index(request):
    return HttpResponse("OK", status=200)

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
