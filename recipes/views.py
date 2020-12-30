from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, CreateView, DeleteView, UpdateView

# from .forms import RecipeForm
from .models import Recipe


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


# @login_required
# def new_recipe(request):
#     pass


class RecipeCreate(LoginRequiredMixin, CreateView):
    model = Recipe
    template_name = "recipe_form.html"
    fields = ["title", "image", "text", "ingredients", "tag", "duration"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class RecipeView(FormView):
    pass

class RecipeUpdate(UpdateView):
    model = Recipe
    template_name = "recipe_form.html"
    fields = ["title", "image", "text", "ingredients", "tag", "duration"]


class RecipeDelete(DeleteView):
    model = Recipe
    success_url = reverse_lazy("recipe-list")
