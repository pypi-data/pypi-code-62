from django import template
from django_ui.models import ThemeUI

register = template.Library()


@register.simple_tag()
def theme_ui():
    return ThemeUI.objects.filter(applied=True).first()
