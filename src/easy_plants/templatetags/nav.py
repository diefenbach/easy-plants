from django import template
from django.urls import reverse

register = template.Library()

MENU_ITEMS = [
    {
        "label": "Home",
        "url": reverse("easy_plants:home"),
    },
    {
        "label": "Archive",
        "url": reverse("easy_plants:archive"),
    },
]


@register.inclusion_tag("easy_plants/nav.html", takes_context=True)
def nav(context, content="content"):
    request = context["request"]

    for menu_item in MENU_ITEMS:
        # First collect all urls from a menu item
        menu_item["sub_urls"] = []
        for sub_item in menu_item.get("menu_items", []):
            menu_item["sub_urls"].append(sub_item["url"])

        # Second check whether there is a sub item active
        sub_active = False
        for sub_url in menu_item.get("sub_urls"):
            if request.path.startswith(sub_url):
                sub_active = True

        # active main items
        if menu_item.get("label") == "Home":
            menu_item["active"] = request.path == reverse("easy_plants:home")
        elif menu_item.get("label") == "Admin":
            menu_item["active"] = request.path == reverse("admin:index")
        elif request.path.startswith(menu_item.get("url", "NO!")) or sub_active:
            menu_item["active"] = True
        else:
            menu_item["active"] = False

        # active sub items
        for sub_item in menu_item.get("menu_items", []):
            if request.path.startswith(sub_item["url"]):
                sub_item["active"] = True
            else:
                sub_item["active"] = False

    return {
        "menu_items": MENU_ITEMS,
        "margin_top": 30 if content == "content" else 60,
    }
