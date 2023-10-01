from django import template
from datetime import timedelta

register = template.Library()


@register.filter
def readable_duration(duration: timedelta, print_format: str):
    days = duration.days
    seconds = duration.seconds
    microseconds = duration.microseconds

    if seconds >= 3600:
        hours = seconds // 3600
        seconds -= hours * 3600
    else:
        hours = 0

    if seconds >= 60:
        minutes = seconds // 60
        seconds -= minutes * 60
    else:
        minutes = 0

    return print_format.format(
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds,
        microseconds=microseconds,
    )
