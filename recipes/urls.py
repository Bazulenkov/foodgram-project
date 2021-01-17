from django.urls import path

from . import views

# app_name = "recipes"

urlpatterns = [
    path("purchases/", views.purchases, name="purchases"),  # список покупок
    # path("purchases/<int:recipe_id>/",),  # ? есть в js.api

    path("subscriptions/", views.subscriptions, name="subscriptions"),  # страница подписок на авторов
    # path("subscriptions/<int:author_id>/",),  # ? есть в js.api

    # path("<username>/",), # страница пользователя (профайл)

    path("recipe/add/", views.RecipeCreate.as_view(), name="new_recipe"),
    path("recipe/<slug:slug>/update", views.RecipeUpdate.as_view(), name="recipe_update"),
    path("recipe/<slug:slug>/delete", views.RecipeDelete.as_view(), name="recipe_delete"),
    path("recipe/<slug:slug>", views.RecipeView.as_view(), name="recipe_view"),

    path("", views.RecipeListView.as_view(), name="index")  # главная страница (все рецепты по дате)
]
