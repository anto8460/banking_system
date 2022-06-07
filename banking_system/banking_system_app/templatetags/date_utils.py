from django import template

register = template.Library()


@register.simple_tag
def european_date(date):
    return date.strftime("%d/%m/%Y %H:%M:%S")
