from django import forms
from django.forms import widgets
from django.forms.widgets import CheckboxSelectMultiple, Widget

# from django.forms.widgets import CheckboxSelectMultiple

from .models import Ingredient, Recipe, Tag, RecipeIngredient


class IngredientMultiWidget(forms.MultiWidget):
    def __init__(self, attrs=None) -> None:
        widgets = {
            forms.TextInput(attrs=attrs),
            forms.TextInput(attrs=attrs),
            forms.TextInput(attrs=attrs),
        }
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.ingredient.title, value.amount, value.ingredient.dimension]
        return ["Nothing", "Nothing", "Nothing"]


class IngredientMultiField(forms.MultiValueField):
    widget = IngredientMultiWidget

    def __init__(self, modelingredient=None, *args, **kwargs) -> None:
            
            fields = (
                forms.fields.CharField(max_length=50),
                forms.fields.CharField(max_length=50),
                forms.fields.CharField(max_length=50),
            )
            super().__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            return data_list
        return ""

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

    def get_ingredients(self, data):  # можно убрать параметр data и дергать из self.request.POST
        result = []
        for key, value in data.items():
            if "nameIngredient" in key:
                nameIngredient = value
            elif "valueIngredient" in key:
                valueIngredient = value
            elif "unitsIngredient" in key:
                ingredient = Ingredient.objects.filter(
                    title=nameIngredient, dimension=value
                ).first()
                result.append([ingredient, valueIngredient])
        return result

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ingredients = RecipeIngredient.objects.filter(recipe=self.instance)
        for i in range(len(ingredients)):
            field_name = "ingredient_%s" % (i,)
            self.fields[field_name] = IngredientMultiField(required=False, modelingredient=ingredients[i], initial=ingredients[i])
            self.fields[field_name].widget.attrs.update({"hidden": True})
        
        # if self.data:
        for ing in self.get_ingredients(self.data):
            i += 1
            field_name = "ingredient_%s" % (i,)
            self.fields[field_name] = IngredientMultiField(required=False)  # здесь надо дописать правильное значение в initial    
            self.fields[field_name].widget.attrs.update({"hidden": True})
            self.initial[field_name] = ing
            # self.initial[]

            # field_nameIngredient = "nameIngredient_%s" % (i,)
            # self.fields[field_nameIngredient] = forms.CharField(required=False)
            # self.fields[field_nameIngredient].widget.attrs.update(
            #     {type: "hidden"}
            # )
            # field_valueIngredient = "valueIngredient_%s" % (i,)
            # self.fields[field_valueIngredient] = forms.CharField(
            #     required=False
            # )
            # field_unitsIngredient = "unitsIngredient_%s" % (i,)
            # self.fields[field_unitsIngredient] = forms.CharField(
            #     required=False
            # )
            # try:
            #     self.initial[field_nameIngredient] = ingredients[
            #         i
            #     ].ingredient.title
            #     self.initial[field_valueIngredient] = ingredients[i].amount
            #     self.initial[field_unitsIngredient] = ingredients[
            #         i
            #     ].ingredient.dimension
            # except IndexError:
            #     self.initial[field_nameIngredient] = ""

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

    # def clean(self):
    #     ingredients = set()
    #     i = 0
    #     field_name = "ingredient_%s" % (i,)
    #     while self.data.get(field_name):
    #         ingredient = self.data[field_name]
    #         if ingredient in ingredients:
    #             self.add_error(field_name, "Duplicate")
    #         else:
    #             ingredients.add(ingredient)
    #         i += 1
    #         field_name = "ingredient_%s" % (i,)
    #     self.cleaned_data["ingredients"] = ingredients

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
            if "ingredient_" in field_name:
                yield self[field_name]
