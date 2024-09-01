import re
from django import template

register = template.Library()

@register.filter
def intspace(value):
    value = str(value)
    return re.sub(r'(?<=\d)(?=(\d{3})+(?!\d))', ' ', value)