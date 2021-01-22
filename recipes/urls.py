from django.urls import path

from . import views

# app_name = "recipes"

urlpatterns = [
    path("purchases/", views.ShopListView.as_view(), name="purchases"),
    path("purchases/<int:recipe_id>/", views.ShopListView.as_view()),
    path("subscriptions/", views.FollowList.as_view(), name="subscriptions"),
    path("subscriptions/<int:author_id>/", views.FollowList.as_view()),
    path("recipe/add/", views.RecipeCreate.as_view(), name="new_recipe"),
    path(
        "recipe/<slug:slug>/update",
        views.RecipeUpdate.as_view(),
        name="recipe_update",
    ),
    path(
        "recipe/<slug:slug>/delete",
        views.RecipeDelete.as_view(),
        name="recipe_delete",
    ),
    path("recipe/<slug:slug>", views.RecipeView.as_view(), name="recipe_view"),
    path("favorites/", views.Favorites.as_view(), name="favorites"),
    path("favorites/<int:recipe_id>/", views.Favorites.as_view()),
    path("<username>/", views.AuthorListView.as_view(), name="author"),
    path("", views.RecipeListView.as_view(), name="index"),
]
