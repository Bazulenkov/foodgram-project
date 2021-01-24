from django.contrib import admin

from .models import Recipe, RecipeIngredient, Ingredient


class RecipeIngredientsInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 2  # how many rows to show


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "favorites_count")
    readonly_fields = ("favorites_count",)
    list_filter = ("author", "title", "tags")
    prepopulated_fields = {"slug": ("title",)}
    inlines = (RecipeIngredientsInline,)
    add_fieldsets = (
        (
            None,
            {
                "fields": ("favorites_count",),
            },
        ),
    )

    def favorites_count(self, obj):
        return obj.favorites.count()


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("title", "dimension")
    list_filter = ("title",)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)