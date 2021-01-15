from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import request
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .forms import RecipeForm
from .models import Recipe, Ingredient, RecipeIngredient


def index(request):
    """Обрабатывает главную страницу"""
    recipe_list = (
        Recipe.objects.select_related("author").order_by("-pub_date").all()
    )
    # показывать по 6 записей на странице.
    paginator = Paginator(recipe_list, 6)
    # переменная в URL с номером запрошенной страницы
    page_number = request.GET.get("page")
    # получить записи с нужным смещением
    page = paginator.get_page(page_number)
    return render(
        request, "index.html", {"page": page, "paginator": paginator}
    )


class RecipeListView(ListView):
    """Выводит список всех рецептов на главную страницу"""

    template_name = "index.html"
    queryset = Recipe.objects.all()
    context_object_name = "recipe_list"
    paginate_by = 6


@login_required
def subscriptions(request):
    """ Выводит список записей авторов, которые есть в подписке """
    recipe_list = Recipe.objects.filter(
        author__following__user=request.user
    ).order_by("-pub_date")
    paginator = Paginator(recipe_list, 3)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(
        request, "myFollow.html", {"page": page, "paginator": paginator}
    )


@login_required
def favorites(request):
    """ Выводит список избранных рецептов """
    # TODO переписать!!!!
    recipe_list = Recipe.objects.filter(
        author__following__user=request.user
    ).order_by("-pub_date")
    paginator = Paginator(recipe_list, 3)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(
        request, "favorite.html", {"page": page, "paginator": paginator}
    )


def purchases(request):
    return render(request, "shopList.html")


class RecipeCreate(LoginRequiredMixin, CreateView):
    # model = Recipe
    form_class = RecipeForm
    template_name = "recipe_form.html"
    # fields = ["title", "tag", "ingredients",  "duration", "description", "image"]

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

    def form_valid(self, form):
        form.instance.author = self.request.user
        # здесь надо создать 
        self.object = form.save()

        # recipeingredients = set()
        # и потом создать записи в таблице RecipeIngredient

        
        # TODO переписать это в save() - чтобы 2 раза не делать form.save()
        #  потом можно сделать через bulk_create() https://docs.djangoproject.com/en/3.0/ref/models/querysets/#bulk-create
        for ingredient in self.get_ingredients(self.request.POST):
            obj, created = RecipeIngredient.objects.get_or_create(recipe=self.object, ingredient=ingredient[0], amount=ingredient[1])
            if not created:
                form.add_error("Duplicate in ingrdients")
            # else:
            #     recipeingredients.add(obj)

        # recipeingredients = RecipeIngredients.objects.filter(recipe=recipe)
        # и потом 
        # form.instance.ingredients_set.add(recipeingredients)

        return super().form_valid(form)

class RecipeView(DetailView):
    model = (
        Recipe  # https://docs.djangoproject.com/en/3.1/ref/class-based-views/
    )
    template_name = "recipe_detail.html"


class RecipeUpdate(UpdateView):
    form_class = RecipeForm
    # model = Recipe
    template_name = "recipe_form.html"
    # fields = ["title", "image", "text", "ingredients", "tag", "duration"]


class RecipeDelete(DeleteView):
    model = Recipe
    success_url = reverse_lazy("recipe-list")
