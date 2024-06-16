from django import template
from ..models import CustomUser

register = template.Library()

@register.filter
def hours_display(value):
    # Extracts the part in parentheses
    start = value.find('(')
    end = value.find(')')
    if start != -1 and end != -1:
        return value[start+1:end]
    return value

@register.filter(name='format_date')
def format_date(value, schedule_format):
    if schedule_format == 'week':
        return value.strftime('%b %d %a')  # Format for week view (Jun 10 Mon)
    elif schedule_format == 'month':
        return value.strftime('%b %d')  # Format for month view (Jun 10)
    else:
        return value.strftime('%H:%M')  # Default format for other views (12:00)
    
@register.filter
def dict_get(value, arg):
    return value.get(arg, [])

@register.filter
def get_user_by_id(user_id):
    return CustomUser.objects.get(id=user_id)

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)