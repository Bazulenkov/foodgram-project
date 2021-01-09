from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple

from .models import Recipe


class RecipeForm(ModelForm):
    """ Форма модели Recipe, добавляем через нее новый рецепт и редактируем имеющющийся рецепт """

    class Meta:
        model = Recipe
        fields = ("title", "tag", "duration", "description", "image")
        localized_fields = "__all__"
        widgets = {"tag": CheckboxSelectMultiple}
