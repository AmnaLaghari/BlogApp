from django.contrib import admin
from PostApp.models import Post
# Register your models here.


@admin.register(Post)
class postAdmin(admin.ModelAdmin):
    pass
