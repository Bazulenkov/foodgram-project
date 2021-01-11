from django.db.models import fields
from rest_framework.serializers import ModelSerializer

from recipes.models import Ingredient

class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["id", "title", "dimension"]
        # read_only_fields = ["title", "dimension"]