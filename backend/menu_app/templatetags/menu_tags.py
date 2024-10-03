from django import template
from django.urls import resolve
from ..models import MenuItem

register = template.Library()

@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    active_url = request.path
    
    # Одновременная загрузка родительских и дочерних элементов
    # prefetch_related позволяет выполнять 1 запрос на отрисовку каждого меню
    menu_items = MenuItem.objects.filter(menu__name=menu_name, parent=None).prefetch_related('children')
    
    def build_menu(items, active_url):
        menu_html = '<ul>'
        for item in items:
            is_active = (
                active_url.startswith(item.url) or
                (item.named_url and resolve(active_url).url_name == item.named_url)
            )

            menu_html += f'<li class="{ "active" if is_active else "" }">'
            menu_html += f'<a href="{item.url or item.named_url}">{item.title}</a>'
            if is_active:
                sub_items = item.children.all()
                if sub_items.exists():
                    menu_html += build_menu(sub_items, active_url)
            menu_html += '</li>'
        menu_html += '</ul>'
        return menu_html

    return build_menu(menu_items, active_url)

# Для сырых SQL запросов для использования метода get_menu_with_items указанного в models.py

# @register.simple_tag(takes_context=True)
# def draw_menu(context, menu_name):
#     request = context['request']
#     active_url = request.path
#     menu_items = MenuItem.get_menu_with_items(menu_name)

#     # Структурируем пункты меню в виде словаря для быстрого доступа
#     menu_dict = {}
#     for item in menu_items:
#         menu_dict[item.id] = {
#             'title': item.title,
#             'url': item.url,
#             'named_url': item.named_url,
#             'parent_id': item.parent_id,
#             'children': []
#         }

#     # Построение меню
#     menu_html = '<ul>'
#     for item in menu_dict.values():
#         if item['parent_id'] is None:  # Если это корневой элемент
#             menu_html += f'<li><a href="{item["url"] or item["named_url"]}">{item["title"]}</a>'
#             # Добавление дочерних элементов
#             children = [child for child in menu_dict.values() if child['parent_id'] == item['id']]
#             if children:
#                 menu_html += '<ul>'
#                 for child in children:
#                     menu_html += f'<li><a href="{child["url"] or child["named_url"]}">{child["title"]}</a></li>'
#                 menu_html += '</ul>'
#             menu_html += '</li>'
#     menu_html += '</ul>'
    
#     return menu_html