from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def translate(value, lang):
    str_list = value.split('|')
    if len(str_list) < 3:
        return value
    if lang == 'ru':
        return str(str_list[0]).strip()
    if lang == 'en':
        return str(str_list[1]).strip()
    return str(str_list[2]).strip()
