from django.contrib import admin

from models import Resipe


class ResipeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Resipe, ResipeAdmin)
