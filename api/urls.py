from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register("ingredients", views.IngredientList, basename="ingredients")

urlpatterns = [
    path("", include(router.urls)),
]
