from django import template
from datetime import datetime
from datetime import date
from pytz import timezone

#Something for the custom filter for searching through a queryset
register = template.Library()


@register.filter
def check_date(value):
    #value = value.replace(tzinfo=utc)
    now = date.today()
    print("Value: " + str(value) + "Now: " + str(now))
    print(value >= now)
    return value >= now

@register.filter
def check_time(value):
    now = datetime.now().time()
    print("Value: " + str(value) + "Now: " + str(now))
    print(value >= now)
    return value >=now

