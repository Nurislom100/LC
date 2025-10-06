from django.contrib import admin

from common import models


@admin.register(models.BaseUser) 
class BaseUserAdmin(admin.ModelAdmin):
    list_display = ["username", "phone", "role"]
    search_fields = ["full_name", "username", "phone"]
