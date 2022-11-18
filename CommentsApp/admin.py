from django.contrib import admin
from .models import Comment, Reply

# Register your models here.
@admin.register(Comment)
class commentAdmin(admin.ModelAdmin):
  pass

@admin.register(Reply)
class replyAdmin(admin.ModelAdmin):
  pass
