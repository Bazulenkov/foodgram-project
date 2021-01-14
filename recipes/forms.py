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
            # "ingredients",
            "duration",
            "description",
            "image",
        )
        localized_fields = "__all__"
        # field_classes = {"tag": MultipleChoiceField}
        # widgets = {"tag": CheckboxSelectMultiple}

    # def __init__(self, data=None, *args, **kwargs):
    #     if data is not None:
    #         data = data.copy()  # make it mutable
    #         # for tag in ("breakfast", "lunch", "dinner"):
    #         #     if tag in data:
    #         #         data.update({"tag": tag})
    #         ingredients = self.get_ingredients(data)
    #         data.update({"ingredients": ingredients})
    #         # for item in ingredients:
    #         # тут про ингридиенты
    #     super().__init__(data=data, *args, **kwargs)
        # self.fields["duration"].widget.attrs.update({"class": "form__input"})



    # def clean_ingredients(self):
    #     data = self.cleaned_data["ingredients"]
    #     return data

    def form_valid(self, form):
        ingredients = self.get_ingredients(data)

                # recipe_ingredient = RecipeIngredient.objects.create(recipe=, ingredient=ingredient, amount=valueIngredient)
                # # or
                # recipe_ingredient = RecipeIngredient(ingredient=ingredient, amount=valueIngredient)
                # recipe_ingredient.save()
