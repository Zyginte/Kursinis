from django import template

register = template.Library()

@register.filter
def hours_display(value):
    # Extracts the part in parentheses
    start = value.find('(')
    end = value.find(')')
    if start != -1 and end != -1:
        return value[start+1:end]
    return value