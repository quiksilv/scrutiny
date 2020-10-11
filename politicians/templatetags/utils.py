from django import template

register = template.Library()

@register.filter
def human_readable(value):
    return value.replace('_', ' ')
