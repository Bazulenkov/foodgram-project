from django import forms
from django.forms import widgets
from django.forms.widgets import CheckboxSelectMultiple, Widget

# from django.forms.widgets import CheckboxSelectMultiple

from .models import Ingredient, Recipe, Tag, RecipeIngredient


class RecipeForm(forms.ModelForm):
    """ Форма модели Recipe, добавляем через нее новый рецепт и редактируем имеющющийся рецепт """

    tag = forms.ModelMultipleChoiceField(
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ingredients = RecipeIngredient.objects.filter(recipe=self.instance)
        for i in range(len(ingredients)):
            field_nameIngredient = "nameIngredient_%s" % (i,)
            # self.fields[field_name] = forms.CharField(required=False)
            field_valueIngredient = "valueIngredient_%s" % (i,)
            field_unitsIngredient = "unitsIngredient_%s" % (i,)
            try:
                self.initial[field_nameIngredient] = ingredients[i].ingredient.title
                self.initial[field_valueIngredient] = ingredients[i].amount
                self.initial[field_unitsIngredient] = ingredients[i].ingredient.dimension
            except IndexError:
                self.initial[field_nameIngredient] = ""

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

    def clean(self):
        ingredients = set()
        i = 0
        field_name = "ingredient_%s" % (i,)
        while self.cleaned_data.get(field_name):
            ingredient = self.cleaned_data[field_name]
            if ingredient in ingredients:
                self.add_error(field_name, 'Duplicate')
            else:
               ingredients.add(ingredient)
            i += 1
            field_name = 'ingredient_%s' % (i,)
        self.cleaned_data["ingredients"] = ingredients

    # def clean_ingredients(self):
    #     data = self.cleaned_data["ingredients"]
    #     return data

    # def save(self):
    #     recipe = self.instance
    #     recipe.author = self.cleaned_data("author")
    #     recipe.title = self.cleaned_data("title")
    #     recipe.tag = self.cleaned_data("tag")
    #     recipe.description = self.cleaned_data("description")
    #     recipe.duration = self.cleaned_data("duration")
    #     recipe.image = self.cleaned_data("image")

    #     recipe.ingredients_set.all().delete()
    #     for ingredient in self.cleaned_data["ingredients"]:
    #         RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient[0], amount=ingredient[1])

    def get_ingredients_fields(self):
        for field_name in self.fields:
            if field_name.contains("ingredient_"):
                yield self(field_name)
