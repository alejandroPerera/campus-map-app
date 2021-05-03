from django import template
import datetime
from datetime import date
from pytz import timezone

#Something for the custom filter for searching through a queryset
register = template.Library()
eastern = timezone('US/Eastern')
central = timezone('US/Central')


@register.filter
def check_date(value):
    #value = value.replace(tzinfo=utc)
    now = date.today()
    print("Value: " + str(value) + "Now: " + str(now))
    print(value >= now)
    return value >= now

