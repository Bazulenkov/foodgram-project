from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register("ingredients", views.IngredientList, basename="ingredients")

urlpatterns = [
    # path("ingredients/",),  # ? есть в js.api
    path("favorites/", views.Favorites.as_view(), name="favorites"),  # список избранных рецептов
    path(
        "favorites/<int:recipe_id>/", views.Favorites.as_view()
    ),  # ? есть в js.api

    path("", include(router.urls)),
]
