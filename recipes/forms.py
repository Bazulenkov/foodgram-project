from django.forms import ModelForm, MultipleChoiceField
from django.forms.widgets import CheckboxSelectMultiple

from .models import Recipe


class RecipeForm(ModelForm):
    """ Форма модели Recipe, добавляем через нее новый рецепт и редактируем имеющющийся рецепт """

    TAG_CHOICES = [
        ('b', 'Breakfast'),
        ('l', 'Lunch'),
        ('d', 'Dinner')
    ]
    tag = MultipleChoiceField(
        widget=CheckboxSelectMultiple,
        choices=TAG_CHOICES
    )

    class Meta:
        model = Recipe
        fields = ("title", "duration", "description", "image")
        localized_fields = "__all__"
