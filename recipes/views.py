from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render

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
        request, "follow.html", {"page": page, "paginator": paginator}
    )
