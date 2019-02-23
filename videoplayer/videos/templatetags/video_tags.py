# Django imports
from django import template

register = template.Library()

@register.filter(name='convert_to_hhmmss')
def convert_to_hhmmss(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    if len(str(h)) == 1 and h!=0:
        h = '0' + str(h)
    if len(str(m)) == 1:
        m = '0' + str(m)
    if len(str(s)) == 1:
        s = '0' + str(s)
    result = str(m) + ":"+ str(s)
    if h:
        result = str(h) + ":" + result
    return result

