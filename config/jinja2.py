# config/jinja2.py

from jinja2 import Environment
from django.urls import reverse

def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'url': lambda name, **kwargs: reverse(name, kwargs=kwargs),
    })
    return env
