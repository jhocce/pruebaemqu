from django.contrib import admin
from .models import user, Token
# Register your models here.

admin.site.register(user)
admin.site.register(Token)