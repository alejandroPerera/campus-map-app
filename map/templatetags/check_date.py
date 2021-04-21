from django import template
import datetime
import pytz

#Something for the custom filter for searching through a queryset
register = template.Library()
utc=pytz.UTC

@register.filter
def check_date(value):
    value = value.replace(tzinfo=utc)
    return value >= datetime.datetime.now().replace(tzinfo=utc)

