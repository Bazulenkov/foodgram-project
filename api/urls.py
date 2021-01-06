from django.urls import path

from . import views

urlpatterns = [
    # path("ingredients/",),  # ? есть в js.api
    path("favorites/", views.Favorites.as_view()),  # список избранных рецептов
    path(
        "favorites/<int:recipe_id>/", views.Favorites.as_view()
    ),  # ? есть в js.api
]
