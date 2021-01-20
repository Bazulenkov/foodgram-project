from django import template

# В template.Library зарегистрированы все теги и фильтры шаблонов
# добавляем к ним и наш фильтр
register = template.Library()


@register.filter
def get_filter_values(get_params):
    if "tags" in get_params:
        return get_params.get("tags")


@register.filter
def get_filter_link(request, tag):
    tags = request.GET.get("tags")
    result : str = tags
    if tags and tag.slug in tags:
        tags = tags.split(",")

        result = 
    return tag.slug