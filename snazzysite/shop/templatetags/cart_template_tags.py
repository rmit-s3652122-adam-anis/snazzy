from django import template
from shop.models import Order

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(buyer=user, ordered=False)
        if qs.exists():
            return qs[0].order_products.count()
    return 0