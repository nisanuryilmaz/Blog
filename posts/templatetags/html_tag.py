from django import template

register = template.Library()


@register.filter
def post_count(post_list):
    return len(post_list)