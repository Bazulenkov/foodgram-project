import json

import weasyprint
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .forms import RecipeForm
from .mixins import ShopListMixin
from .models import Favorite, Follow, Recipe, RecipeIngredient, Tag, User
from .shoplist import ShopList


class RecipeListView(ShopListMixin, ListView):
    """Выводит список всех рецептов на главную страницу."""

    template_name = "index.html"
    model = Recipe
    context_object_name = "recipe_list"
    paginate_by = 6

    def __init__(self, **kwargs) -> None:
        self.all_tags = Tag.objects.all()
        super().__init__(**kwargs)

    def get_queryset(self):  # -> QuerySet:
        queryset = super().get_queryset()

        tags = self.request.GET.getlist("tags")
        all_tags = [tag.slug for tag in self.all_tags]
        tags = list(set(all_tags) - set(tags))
        if tags:
            queryset = queryset.filter(tags__slug__in=tags).distinct()

        return queryset


class AuthorListView(RecipeListView):
    """Выводит список всех рецептов одного автора."""

    def get_queryset(self):
        self.author = get_object_or_404(
            User, username=self.kwargs.get("username")
        )
        self.queryset = self.model._default_manager.filter(author=self.author)
        return super().get_queryset()


class FollowList(ShopListMixin, LoginRequiredMixin, ListView):
    """Добавляет/удаляет автора в подписки + отображение."""

    template_name = "follow.html"
    paginate_by = 3

    def get_queryset(self):  # -> QuerySet:
        queryset = User.objects.filter(following__user=self.request.user)
        return queryset

    def post(self, request):
        """Обрабатывает POST-запрос от JS при нажатии на кнопку \
            "Подписаться"."""
        req_ = json.loads(request.body)
        author_id = req_.get("id")
        if author_id is not None:
            author = get_object_or_404(User, id=author_id)
            obj, created = Follow.objects.get_or_create(
                user=request.user, author=author
            )
            return JsonResponse({"success": created})
        return JsonResponse({"success": False}, status=400)

    def delete(self, request, author_id):
        """Обрабатывает POST-запрос от JS при нажатии на кнопку \
            "Отписаться"."""
        author = get_object_or_404(Follow, user=request.user, author=author_id)
        author.delete()
        return JsonResponse({"success": True})


class Favorites(LoginRequiredMixin, RecipeListView):
    """Добавляет/удаляет рецепта в "Избранное" + отображение."""

    def get_queryset(self):
        self.queryset = self.model._default_manager.filter(
            favorites__user=self.request.user
        )
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["favorites"] = True
        return context

    def post(self, request):
        """Обрабатывает POST-запрос от JS при нажатии на "звездочку"."""
        req_ = json.loads(request.body)
        recipe_id = req_.get("id")
        if recipe_id is not None:
            recipe = get_object_or_404(Recipe, id=recipe_id)
            obj, created = Favorite.objects.get_or_create(
                user=request.user, recipe=recipe
            )
            return JsonResponse({"success": created})
        return JsonResponse({"success": False}, status=400)

    def delete(self, request, recipe_id):
        """Обрабатывает POST-запрос от JS при отжатии "звездочки"."""
        recipe = get_object_or_404(
            Favorite, user=request.user, recipe=recipe_id
        )
        recipe.delete()
        return JsonResponse({"success": True})


class ShopListView(ShopListMixin, ListView):
    """Добавляет/удаляет рецепты в список покупок + отображение."""

    template_name = "shop_list.html"
    model = Recipe
    context_object_name = "recipe_list"

    def get_queryset(self):  # -> QuerySet:
        shoplist = ShopList(self.request)
        queryset = Recipe.objects.filter(id__in=shoplist.shoplist)
        return queryset

    def post(self, request):
        """Обрабатывает POST-запрос от JS. Добавляет рецепт в список \
            покупок."""
        req_ = json.loads(request.body)
        shoplist = ShopList(request)
        recipe_id = req_.get("id")
        if recipe_id is not None:
            shoplist.add(int(recipe_id))
            return JsonResponse({"success": True})
        return JsonResponse({"success": False}, status=400)

    def delete(self, request, recipe_id):
        """Обрабатывает POST-запрос от JS. Удаляет рецепт из спика покупок."""
        shoplist = ShopList(request)
        shoplist.remove(int(recipe_id))
        return JsonResponse({"success": True})


def order_pdf(request):
    """Формирует pdf-файл со списком ингредиентов для покупки."""
    shoplist = ShopList(request)
    recipe_list = Recipe.objects.filter(id__in=shoplist.shoplist)
    ingredient_list = (
        RecipeIngredient.objects.filter(recipe__id__in=shoplist.shoplist)
        .values("ingredient__title", "ingredient__dimension")
        .annotate(amountsum=Sum("amount"))
    )

    html = render_to_string(
        "shoppinglist_pdf.html",
        {"recipe_list": recipe_list, "ingredients": ingredient_list},
    )
    response = HttpResponse(content_type="application/pdf")
    response[
        "Content-Disposition"
    ] = 'filename=\
    "list_{}.pdf"'.format(
        request.user.id
    )
    weasyprint.HTML(string=html).write_pdf(
        response,
        stylesheets=[
            weasyprint.CSS(str(settings.STATIC_ROOT) + "/shoppinglist_pdf.css")
        ],
    )
    return response


class RecipeCreate(ShopListMixin, LoginRequiredMixin, CreateView):
    """Создание рецепта."""

    form_class = RecipeForm
    template_name = "recipe_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecipeView(ShopListMixin, DetailView):
    """Отображение рецепта детально."""

    model = Recipe
    template_name = "recipe_detail.html"


class RecipeUpdate(ShopListMixin, LoginRequiredMixin, UpdateView):
    """Редактирование рецепта."""

    form_class = RecipeForm
    model = Recipe
    template_name = "recipe_form.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user != self.object.author:
            return redirect(self.object.get_absolute_url())
        return super().get(request, *args, **kwargs)


class RecipeDelete(ShopListMixin, DeleteView):
    """Удаление рецепта."""

    model = Recipe
    template_name = "recipe_congirm_delete.html"
    success_url = reverse_lazy("index")

    def post(self, request, *args: str, **kwargs):
        shoplist = ShopList(request)
        recipe = get_object_or_404(Recipe, slug=kwargs["slug"])
        recipe_id: int = recipe.id
        if recipe_id in shoplist.shoplist:
            shoplist.remove(recipe_id)
        return super().post(request, *args, **kwargs)
