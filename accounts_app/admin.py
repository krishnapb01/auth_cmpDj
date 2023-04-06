from django.contrib import admin

from .models import Profile
# Register your models here.

@admin.register(Profile)
class ProfileModel(admin.ModelAdmin):
   list_display = ('id', 'user', 'bio')