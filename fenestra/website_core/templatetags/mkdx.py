from django import template
from markdownx.utils import markdownify

register = template.Library()


@register.filter
def mkdx(text):
    return markdownify(text)
