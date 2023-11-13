from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    
    # add rule url
    path("api/add_rule/", views.add_rule, name="add_rule"),
]