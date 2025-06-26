from django.contrib import admin
from users.models import CustomUser
# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    list_filter = ('first_name', 'last_name')
admin.site.register(CustomUser, CustomUserAdmin)
