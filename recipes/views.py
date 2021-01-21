from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import request
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .forms import RecipeForm
from .models import Recipe, Ingredient, RecipeIngredient, Tag, User


# def index(request):
#     """Обрабатывает главную страницу"""
#     recipe_list = (
#         Recipe.objects.select_related("author").order_by("-pub_date").all()
#     )
#     # показывать по 6 записей на странице.
#     paginator = Paginator(recipe_list, 6)
#     # переменная в URL с номером запрошенной страницы
#     page_number = request.GET.get("page")
#     # получить записи с нужным смещением
#     page = paginator.get_page(page_number)
#     return render(
#         request, "index.html", {"page": page, "paginator": paginator}
#     )


class RecipeListView(ListView):
    """Выводит список всех рецептов на главную страницу"""

    template_name = "index.html"
    model = Recipe
    context_object_name = "recipe_list"
    paginate_by = 6

    def __init__(self, **kwargs) -> None:
        self.all_tags = Tag.objects.all()
        super().__init__(**kwargs)

    def get_queryset(self):  # -> QuerySet:
        queryself = super().get_queryset()

        tags = self.request.GET.getlist("tags")
        all_tags = [tag.slug for tag in self.all_tags]
        tags = list(set(all_tags) - set(tags))
        if tags:
            self.queryset = queryself.filter(tags__slug__in=tags).distinct()

        return queryself

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # Add in a QuerySet of all the books
    #     context["all_tags"] = Tag.objects.all()
    #     return context


class AuthorListView(RecipeListView):
    """Выводит список всех рецептов одного автора"""

    def get_queryset(self):
        self.author = get_object_or_404(
            User, username=self.kwargs.get("username")
        )
        self.queryset = self.model._default_manager.filter(author=self.author)
        return super().get_queryset()


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

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecipeView(DetailView):
    model = (
        Recipe  # https://docs.djangoproject.com/en/3.1/ref/class-based-views/
    )
    template_name = "recipe_detail.html"


class RecipeUpdate(LoginRequiredMixin, UpdateView):
    form_class = RecipeForm
    model = Recipe
    template_name = "recipe_form.html"
    # fields = ["title", "image", "text", "ingredients", "tag", "duration"]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user != self.object.author:
            return redirect(self.object.get_absolute_url())
        return super().get(request, *args, **kwargs)


class RecipeDelete(DeleteView):
    model = Recipe
    success_url = reverse_lazy("recipe-list")
