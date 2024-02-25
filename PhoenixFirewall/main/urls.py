from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("success", views.add_success, name="add_success"),
    # Config was uploaded successfully
    path("success_config/", views.config_sucess_resp, name="config_success_resp"),
    #log in url
    path("login/", views.login_view, name ="login"),
    # add rule url
    path("add_rule/", views.add_rule, name="add_rule"),
    # delete rule url
    path("delete_rule/", views.delete_rule, name="delete_rule"),
    #user url
    path("user/", views.user_view, name="user"),
    #download config
    path("get_pan_security_config/", views.get_pan_security_config, name="get_pan_security_config")
]
