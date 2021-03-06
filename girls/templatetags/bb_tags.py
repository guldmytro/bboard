from django import template
from django.template.defaultfilters import stringfilter
import re

register = template.Library()


@register.filter
@stringfilter
def phone_to_link(value):
    tel = re.sub('[^0-9]', '', value)
    return f'tel:+{tel}'


@register.filter
@stringfilter
def phone_clear(value):
    tel = re.sub('[^0-9]', '', value)
    return tel


@register.filter
@stringfilter
def whatsapp(value):
    tel = re.sub('[^0-9]', '', value)
    return f'https://wa.me/{tel}'

