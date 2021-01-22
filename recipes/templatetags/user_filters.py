from django import template
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

# В template.Library зарегистрированы все теги и фильтры шаблонов
# добавляем к ним и наш фильтр
register = template.Library()

User = get_user_model()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def is_favorite(recipe_id, user):
    result = user.favorites.filter(recipe=recipe_id).exists()
    return result

@register.filter
def has_follower(author_id, user):
    result = user.follower.filter(author=author_id).exists()
    return result

@register.filter
def in_purchases(recipe_id, user):
    result = user.purchases.filter(recipe=recipe_id).exists()
    return result