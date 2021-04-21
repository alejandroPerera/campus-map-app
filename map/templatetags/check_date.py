from django import template
import datetime
from pytz import timezone

#Something for the custom filter for searching through a queryset
register = template.Library()
eastern = timezone('US/Eastern')
central = timezone('US/Central')


@register.filter
def check_date(value):
    #value = value.replace(tzinfo=utc)
    now = datetime.datetime.now().replace(tzinfo=eastern)
    value = value.astimezone(central)
    print("Value: " + str(value) + "Now: " + str(now))
    print(value >= now)
    return value >= now

