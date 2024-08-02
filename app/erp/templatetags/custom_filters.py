from django import template
from django.utils.translation import gettext_lazy as _

register = template.Library()


@register.filter
def trans(value):
    return _(value)

