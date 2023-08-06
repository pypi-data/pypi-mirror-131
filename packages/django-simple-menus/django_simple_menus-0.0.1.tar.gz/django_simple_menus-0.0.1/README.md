# Django Simple Menus

Simple Menus For Django / Wagtail.

Install:

```shell
pip install django-simple-menus
```

Add template loader

```python
# settings.py
INSTALLED_APPS [
    ...
    'simple_menus',
    'mptt'
    ...
]
```

Usage in template

```html
{% load simplemenus_tags %}

{% render_menu 'main_menu' %}

```
