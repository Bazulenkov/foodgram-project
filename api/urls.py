from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("ingredients", views.IngredientList, basename="ingredients")

urlpatterns = [
    path("v1/", include(router.urls)),
]
