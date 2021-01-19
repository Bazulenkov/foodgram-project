from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import RecipeUser

admin.site.register(RecipeUser, UserAdmin)
