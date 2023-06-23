from django import template

register = template.Library()


@register.filter
def get_last_element(value, delimiter):
    parts = value.strip('/').split(delimiter)
    return parts[-1]