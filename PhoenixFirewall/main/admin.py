from django.contrib import admin

# Register your models here.
from .models import userlogIn
from .models import Rule

admin.site.register(userlogIn)
admin.site.register(Rule)