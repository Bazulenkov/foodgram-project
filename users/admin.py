from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import RecipeUser


class RecipeUserAdmin(UserAdmin):
    list_filter = ("username", "email")


admin.site.register(RecipeUser, RecipeUserAdmin)
