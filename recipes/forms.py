from django.forms import ModelForm

from .models import Recipe
class RecipeForm(ModelForm):
    """ Форма модели Recipe, добавляем через нее новый рецепт и редактируем имеющющийся рецепт """
    class Meta:
        model = Recipe
        # fields = ('group', 'text', 'image')
        localized_fields = '__all__'