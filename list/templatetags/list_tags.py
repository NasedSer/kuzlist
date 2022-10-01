from django import template

from list.models import *

register = template.Library()


@register.simple_tag()
def get_files_by_oks_id(oks_id):
    return Files.objects.filter(oks=oks_id)


@register.simple_tag()
def get_tips(filter=None):
    if not filter:
        return Tip.objects.all()
    else:
        return Tip.objects.filter(pk=filter)


@register.inclusion_tag('list/list_tips.html')
def show_tips(tip_select=0):
    if tip_select>0:
        tips = Tip.objects.filter(pk=tip_select)
    else:
        tips = Tip.objects.all()
    return {"tips": tips, 'tip_select': tip_select}


@register.inclusion_tag('list/menu.html')
def show_menu(user_is_login=False):
    menu = [{'title': "Перечень", 'url_name': 'home', 'icon_name': 'fa fa-home'},
            {'title': "Перечень", 'url_name': 'home', 'icon_name': 'fa fa-home'},
            {'title': "Объекты", 'url_name': 'home', 'icon_name': 'fa fa-university', 'sub_menu': [
                {'title': "Добавить объект", 'url_name': 'add_obj_inline'},
                {'title': "Добавить объект в перечень", 'url_name': 'add_obj_to_per'},
            ]},
            {'title': "Admin", 'url_name': 'admin:index', 'icon_name': 'fa fa-university'},
            {'title': "Войти", 'url_name': 'login', 'icon_name': 'fa fa-sign-in'},
            {'title': "Выйти", 'url_name': 'logout', 'icon_name': 'fa fa-sign-out'},
            ]
    if not user_is_login:
        menu.pop(5)
        menu.pop(3)
        menu.pop(2)
        menu.pop(1)
    else:
        menu.pop(4)
        menu.pop(0)
    return {"menu": menu, }


@register.simple_tag()
def my_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)

    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0]!=field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)

    return url


@register.filter
def adjust_for_pagination(value, start):
    value, page = int(value), int(start)
    adjusted_value = value + start - 1
    return adjusted_value