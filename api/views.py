from rest_framework.viewsets import ReadOnlyModelViewSet

from api.serializers import IngredientSerializer
from recipes.models import Ingredient


class IngredientList(ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer

    def get_queryset(self):
        url_parameter = self.request.GET.get("query")
        queryset = Ingredient.objects.filter(title__istartswith=url_parameter)
        return queryset
