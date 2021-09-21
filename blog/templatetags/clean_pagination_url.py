from django import template

register = template.Library()

@register.filter
def clean_pagination_url(url):
    if '&page=' in url:
        root_url, rest = url.split('&page=')
        return root_url
    else:
        return url
