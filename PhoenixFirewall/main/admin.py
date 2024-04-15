from django.contrib import admin

# Register your models here.
from .models import userlogIn
from .models import Rule
# from .models import DeleteRule

admin.site.register(userlogIn)
admin.site.register(Rule)
# admin.site.register(DeleteRule)