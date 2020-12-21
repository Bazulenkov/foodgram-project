from django.core.paginator import Paginator
from django.shortcuts import render

from .models import Recipe


def index(request):
    """Обрабатывает главную страницу"""
    recipe_list = (
        Recipe.objects.select_related("author").order_by("-pub_date").all()
    )
    # показывать по 10 записей на странице.
    paginator = Paginator(recipe_list, 10)
    # переменная в URL с номером запрошенной страницы
    page_number = request.GET.get("page")
    # получить записи с нужным смещением
    page = paginator.get_page(page_number)
    return render(
        request, "index.html", {"page": page, "paginator": paginator}
    )
