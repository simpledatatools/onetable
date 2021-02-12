from django import template

register = template.Library()


@register.filter('get_range')
def get_range(value):
    return range(int(value))


@register.filter('get_range_other')
def get_range_other(value, other=5):
    return range(int(value), other)


@register.filter('star_rating_value')
def star_rating_value(value, other):
    if int(value) >= int(other):
        return True
