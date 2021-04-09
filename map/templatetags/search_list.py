from django import template

#Something for the custom filter for searching through a queryset
register = template.Library()

@register.filter
def in_list(value,arg):
   return value in arg