from django import template
from datetime import datetime

register = template.Library()

@register.simple_tag
def european_date(date):
    return date.strftime("%d/%m/%Y %H:%M:%S")