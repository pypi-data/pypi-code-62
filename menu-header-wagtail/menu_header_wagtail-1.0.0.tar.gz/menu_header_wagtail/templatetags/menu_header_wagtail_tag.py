from django import template

register = template.Library()


@register.inclusion_tag('menu_header_wagtail/header_block.html', takes_context=True, )
def render_header_ui(context, page):
    if page:
        context['page'] = page
    return context


@register.simple_tag
def is_menu_item_dropdown(value):
    return \
        len(value.get('sub_links', [])) > 0 or \
        (
                value.get('show_child_links', False) and len(value.get('page', []).get_children().live()) > 0
        )


@register.simple_tag()
def get_parent_page(page):
    return page.get_parent()
