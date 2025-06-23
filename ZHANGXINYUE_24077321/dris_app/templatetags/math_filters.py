from django import template

register = template.Library()

@register.filter(name='div')
def div(value, arg):
    """除法过滤器"""
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return 0

@register.filter(name='percentage')
def percentage(value, arg):
    """计算百分比"""
    try:
        return f"{float(value) / float(arg) * 100:.2f}%"
    except (ValueError, ZeroDivisionError):
        return "0.00%"


@register.filter(name='multiply')
def multiply(value, arg):
    """乘法过滤器"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0