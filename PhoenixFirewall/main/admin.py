from django.contrib import admin

from .models import userlogIn  # import the userlogIn model
from .models import Rule  # import the Rule model

admin.site.register(userlogIn)  # register the userlogIn model with the admin site
admin.site.register(Rule)  # register the Rule model with the admin site
