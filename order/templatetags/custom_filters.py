import base64
from django import template

register = template.Library()

@register.filter
def base64encode(value):
    """Converts binary data to base64."""
    return base64.b64encode(value).decode('utf-8')
