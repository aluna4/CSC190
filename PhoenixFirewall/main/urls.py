from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    #log in url
    path("log_in/", views.log_in, name ="log_in"),
    # add rule url
    path("add_rule/", views.add_rule, name="add_rule")
    
    ,
]