from django.utils.translation import gettext_lazy as _
from django.template import Library
from simple_menus.models import Menu

register = Library()


@register.simple_tag(takes_context=True)
def render_menu(context, menu_slug):
    request = context["request"]
    menu = Menu.objects.filter(slug=menu_slug).first()
    if menu:
        return menu.render_html(request, context={})
    else:
        return _("Menu `%s` doesn't exist!" % menu_slug)
