from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    #log in url
    path("login/", views.login_view, name ="login"),
    # add rule url
    path("add_rule/", views.add_rule, name="add_rule")
]