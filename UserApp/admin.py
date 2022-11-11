from django.contrib import admin
from UserApp.models import CustomUser

@admin.register(CustomUser)
class customuserAdmin(admin.ModelAdmin):
    pass
