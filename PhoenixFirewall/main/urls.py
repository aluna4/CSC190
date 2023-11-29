from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    
    # add rule url
    path("add_rule/", views.add_rule, name="add_rule"),
    path("login/", views.login_view, name="login")
]