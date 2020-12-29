from django.urls import path

from . import views

urlpatterns = [
    path("purchases/", views.purchases, name="purchases"),  # список покупок
    # path("purchases/<int:recipe_id>/",),  # ? есть в js.api

    path("subscriptions/", views.subscriptions, name="subscriptions"),  # страница подписок на авторов
    # path("subscriptions/<int:author_id>/",),  # ? есть в js.api
    
    path("favorites/", views.favorites, name="favorites"),  # список избранных рецептов
    # path("favorites/<int:recipe_id>/",),  # ? есть в js.api
    
    # path("ingredients/",),  # ? есть в js.api
    
    # path("<username>/",), # страница пользователя (профайл)
    
    path("recipe/new/", views.RecipeView.as_view(), name="new_recipe"),
    # path("reсipe/<slug:slug>/",),  # страница рецепта
    
    path("", views.index, name="index")  # главная страница (все рецепты по дате)
]