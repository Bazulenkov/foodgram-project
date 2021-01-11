from django.forms import ModelForm, MultipleChoiceField
from django.forms.widgets import CheckboxSelectMultiple

from .models import Recipe


class RecipeForm(ModelForm):
    """ Форма модели Recipe, добавляем через нее новый рецепт и редактируем имеющющийся рецепт """

    TAG_CHOICES = [
        ("breakfast", "Breakfast"),
        ("lunch", "Lunch"),
        ("dinner", "Dinner"),
    ]

    tag = MultipleChoiceField(
        # required=False, 
        # widget=CheckboxSelectMultiple, 
        choices=TAG_CHOICES
    )

    class Meta:
        model = Recipe
        fields = ("title", "tag", "duration", "description", "image")
        localized_fields = "__all__"
        # field_classes = {"tag": MultipleChoiceField}
        # widgets = {"tag": CheckboxSelectMultiple}

    def __init__(self, data=None, *args, **kwargs):
        if data is not None:
            data = data.copy() # make it mutable
            for tag in ("breakfast", "lunch", "dinner"):
               if tag in data:
                   data.update({"tag": tag})
            # ingredients = self.get_ingredients(data)
            # for item in ingredients:
              #тут про ингридиенты        
        super().__init__(data=data, *args, **kwargs)
        self.fields["duration", "description"].widget.attrs.update({"class": ""})
