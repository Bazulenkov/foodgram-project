from api.serializers import IngredientSerializer
import json
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework.viewsets import ReadOnlyModelViewSet

from recipes.models import Follow, Ingredient, Favorite, Recipe

User = get_user_model()


class Favorites(LoginRequiredMixin, View):
    """Функция добавления/удаления рецепта в "Избранное"."""

    def get(self, request):
        pass

    def post(self, request):
        req_ = json.loads(request.body)
        recipe_id = req_.get("id", None)
        if recipe_id is not None:
            recipe = get_object_or_404(Recipe, id=recipe_id)
            obj, created = Favorite.objects.get_or_create(
                user=request.user, recipe=recipe
            )

            if created:
                return JsonResponse({"success": True})
            return JsonResponse({"success": False})
        return JsonResponse({"success": False}, status=400)

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(
            Favorite, user=request.user, recipe=recipe_id
        )
        recipe.delete()
        return JsonResponse({"success": True})


class IngredientList(ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer

    def get_queryset(self):
        url_parameter = self.request.GET.get("query")
        queryset = Ingredient.objects.filter(title__startswith=url_parameter)
        return queryset
