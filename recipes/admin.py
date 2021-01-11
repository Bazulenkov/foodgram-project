from django.contrib import admin

from .models import Recipe, RecipeIngredient


class RecipeIngredientsInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 2  # how many rows to show


class RecipeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    inlines = (RecipeIngredientsInline,)


admin.site.register(Recipe, RecipeAdmin)
