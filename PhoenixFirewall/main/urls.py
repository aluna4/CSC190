from django.urls import path
from . import views

# list of URL patterns for mapping URLs to view functions
urlpatterns = [
    path("", views.home, name="home"),
    path("success", views.add_success, name="add_success"),
    # successful config upload url
    path("success_config/", views.config_sucess_resp, name="config_success_resp"),
    # log in url
    path("login/", views.login_view, name ="login"),
    # add rule url
    path("add_rule/", views.add_rule, name="add_rule"),
    # delete rule url
    path("delete_rule/", views.delete_rule, name="delete_rule"),
    # commit rule url
    path("commit_rule/", views.commit_rule, name="commit_rule"),
    # user url
    path("user/", views.user_view, name="user"),
    # admin url
    path("custom-admin/", views.custom_admin_view, name="custom_admin"),
    # download config url
    path("get_pan_security_config/", views.get_pan_security_config, name="get_pan_security_config"),
    path("upload/", views.upload, name="upload"),
    # create user url
    path("create_user/", views.create_user_view, name="create_user"),
]
