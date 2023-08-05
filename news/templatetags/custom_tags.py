from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
   d = context['request'].GET.copy()
   for k, v in kwargs.items():
       d[k] = v
   return d.urlencode()

@register.simple_tag(takes_context=True)
def url_replace2(context, **kwargs):
   p = context['request'].path
   return p[0:-6]

@register.simple_tag(takes_context=True)
def url_replace3(context, **kwargs):
   t = context['request'].path
   return t[0:-7]