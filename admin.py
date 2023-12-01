from django.contrib import admin
from .models import app_password
# Register your models here.

@admin.register(app_password)
class AppPasswordAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']
