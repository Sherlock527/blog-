from django.template import Library

register = Library()


# 使用装饰器注册，以filter('multiply')中的名字为准
# 该名字会和函数def multiply(a, b)对应起来
# 函数只能1到2个参数，其中1个参数形式是{{i|multiply}}
@register.filter('multiply')
def multiply(a, b):
    return int(a) * int(b)
