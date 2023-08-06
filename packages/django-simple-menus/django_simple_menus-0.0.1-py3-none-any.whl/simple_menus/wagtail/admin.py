from wagtail.admin.edit_handlers import FieldPanel, ObjectList
from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup
from wagtail.contrib.modeladmin.options import modeladmin_register

from simple_menus.models import Menu, MenuItem


class MenuAdmin(ModelAdmin):
    model = Menu


class MenuItemAdmin(ModelAdmin):
    model = MenuItem

    edit_handler = ObjectList(
        [
            FieldPanel("parent"),
            FieldPanel("label"),
            FieldPanel("slug"),
            FieldPanel("url"),
            FieldPanel("order"),
            FieldPanel("icon"),
            FieldPanel("classnames"),
            FieldPanel("description"),
            FieldPanel("groups"),
        ]
    )


class MenuAdminGroup(ModelAdminGroup):
    items = (MenuAdmin, MenuItemAdmin)
    menu_label = "Menu"
    menu_order = None
    menu_icon = "form"


modeladmin_register(MenuAdminGroup)
