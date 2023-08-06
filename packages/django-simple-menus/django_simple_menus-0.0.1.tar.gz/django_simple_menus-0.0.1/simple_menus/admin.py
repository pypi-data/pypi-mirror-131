from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Menu, MenuItem


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "menu_root"]


@admin.register(MenuItem)
class MenuItemAdmin(DraggableMPTTAdmin):
    list_display = ("tree_actions", "indented_title", "url")
