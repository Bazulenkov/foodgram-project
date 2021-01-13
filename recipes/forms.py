from django.forms import ModelForm, ModelMultipleChoiceField
from django.forms import widgets
from django.forms.widgets import CheckboxSelectMultiple, Widget
from django.shortcuts import get_object_or_404

# from django.forms.widgets import CheckboxSelectMultiple

from .models import Ingredient, Recipe, Tag, RecipeIngredient


class RecipeForm(ModelForm):
    """ Форма модели Recipe, добавляем через нее новый рецепт и редактируем имеющющийся рецепт """

    tag = ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        to_field_name="slug",
        # widget=CheckboxSelectMultiple,
    )

    class Meta:
        model = Recipe
        fields = (
            "title",
            "tag",
            "ingredients",
            "duration",
            "description",
            "image",
        )
        localized_fields = "__all__"
        # field_classes = {"tag": MultipleChoiceField}
        # widgets = {"tag": CheckboxSelectMultiple}

    def __init__(self, data=None, *args, **kwargs):
        if data is not None:
            data = data.copy()  # make it mutable
            # for tag in ("breakfast", "lunch", "dinner"):
            #     if tag in data:
            #         data.update({"tag": tag})
            ingredients = self.get_ingredients(data)
            # for item in ingredients:
            # тут про ингридиенты
        super().__init__(data=data, *args, **kwargs)
        # self.fields["duration"].widget.attrs.update({"class": "form__input"})

    def get_ingredients(self, data):
        result = []
        for key, value in data.items():
            if "nameIngredient" in key:
                nameIngredient = value
            elif "valueIngredient" in key and nameIngredient:
                valueIngredient = value
            elif "unitsIngredient" in key and nameIngredient and valueIngredient:
                result.append(tuple(nameIngredient, valueIngredient, value))
                nameIngredient = valueIngredient = None
        return result
                
                # ingredient = get_object_or_404(Ingredient, title=nameIngredient, dimension=value)
                # recipe_ingredient = RecipeIngredient.objects.create(recipe=, ingredient=ingredient, amount=valueIngredient)
                # # or
                # recipe_ingredient = RecipeIngredient(ingredient=ingredient, amount=valueIngredient)
                # recipe_ingredient.save()
