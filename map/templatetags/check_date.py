from django import template
from datetime import datetime
from datetime import date
from pytz import timezone

#Something for the custom filter for searching through a queryset
register = template.Library()


@register.filter
def check_date(event):
    #value = value.replace(tzinfo=utc)
    currentDay = date.today()
    print("Value: " + str(event.date) + "Now: " + str(currentDay))
    print(event.date >= currentDay)
    currentTime = datetime.now().time()
    print("Value: " + str(event.time) + "Now: " + str(currentTime))
    print(event.time >= currentTime)
    if(event.date>currentDay):
        return event.date > currentDay
    elif(event.date == currentDay):
        return event.time >= currentTime
    else:
        return False
@register.filter
def check_all_events(eventList):
    for e in eventList:
        if(check_date(e)):
            return True
    return False
# @register.filter
# def check_time(value):
#     now = datetime.now().time()
#     print("Value: " + str(value) + "Now: " + str(now))
#     print(value >= now)
#     return value >=now

