"""
Template tag для рендеринга древовидного меню.
"""
from django import template
from ..models import MenuItem

register = template.Library()


@register.inclusion_tag('menu/menu_tree.html', takes_context=True)
def draw_menu(context, menu_name):
    """
    Рендерит меню с указанным menu_name, учитывая текущий URL.
    Использует один запрос к БД для получения всех пунктов меню.
    """
    request = context['request']
    current_url = request.path_info
    menu_tree = MenuItem.get_menu_tree(menu_name, current_url)
    return {'menu_items': menu_tree, 'current_url': current_url}