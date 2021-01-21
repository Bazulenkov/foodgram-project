from api.serializers import IngredientSerializer
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ReadOnlyModelViewSet

from recipes.models import Ingredient

User = get_user_model()


class IngredientList(ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer

    def get_queryset(self):
        url_parameter = self.request.GET.get("query")
        queryset = Ingredient.objects.filter(title__istartswith=url_parameter)
        return queryset
