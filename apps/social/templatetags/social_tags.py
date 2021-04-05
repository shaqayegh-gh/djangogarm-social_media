from django import template
from datetime import datetime
from apps.social.models import Profile

register = template.Library()


@register.inclusion_tag('social/profile_photo.html')
def profile_photo(user):
    profile = Profile.objects.get(user=user)
    return {'current_profile': profile}


@register.filter()
def today_time_check(list):
    """this filter tag returns the objects(likes and comments) which is created in last 24 hours"""
    filter_list = []
    for item in list:
        time = item.date_created.replace(tzinfo=None)
        difference = datetime.now() - time
        if difference.total_seconds() < 24 * 60 * 60:
            filter_list.append(item)
    return filter_list


@register.filter()
def month_time_check(list):
    """this filter tag returns the objects(likes and comments) which is created in this month"""
    filter_list = []
    for item in list:
        time = item.date_created.replace(tzinfo=None)
        difference = datetime.now() - time
        if 8 <= difference.days < 30:
            filter_list.append(item)
    return filter_list


@register.filter()
def week_time_check(list):
    """this filter tag returns the objects(likes and comments) which is created in this week"""
    filter_list = []
    for item in list:
        time = item.date_created.replace(tzinfo=None)
        difference = datetime.now() - time
        if 24 * 60 * 60 <= difference.total_seconds() and difference.days < 8:
            filter_list.append(item)
    return filter_list
