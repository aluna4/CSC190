from django.urls import path
from . import views


# Calls views.index function which returns 200 status code 
urlpatterns = [
    path("", views.index, name="index")
]