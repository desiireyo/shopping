from django import template
import random

register = template.Library()

def cut(value, arg):
    
    return value.replace(arg, '')

def lower(value): # Only one argument.
    
    return value.lower()

@register.simple_tag
def random_int(a, b=None):
    if b is None:
        a, b = 0, a
    return random.randint(a, b)