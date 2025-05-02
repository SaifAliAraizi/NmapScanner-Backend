# scanner/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, ScanRecord

admin.site.register(CustomUser, UserAdmin)
admin.site.register(ScanRecord)
