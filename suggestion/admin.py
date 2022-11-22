from django.contrib import admin

from .models import Suggestion


# Register your models here.
@admin.register(Suggestion)
class suggestionAdmin(admin.ModelAdmin):
    pass
