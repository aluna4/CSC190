from django.contrib import admin

# Register your models here.
from .models import userlogIn
from .models import AddRule
from .models import DeleteRule

admin.site.register(userlogIn)
admin.site.register(AddRule)
admin.site.register(DeleteRule)