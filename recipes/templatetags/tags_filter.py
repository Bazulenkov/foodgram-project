from django import template

register = template.Library()


@register.filter
def get_filter_values(get_params):
    return get_params.getlist("tags")


@register.filter
def get_filter_link(get_params, tag):
    tags: list = get_params.getlist("tags")
    if tag.slug in tags:
        tags.remove(tag.slug)
    else:
        tags.append(tag.slug)

    if tags:
        result = "tags=" + "&tags=".join(tags)
        return result


@register.filter
def get_tags(get_params):
    tags = get_params.getlist("tags")
    if tags:
        result = "tags=" + "&tags=".join(tags)
        return result
