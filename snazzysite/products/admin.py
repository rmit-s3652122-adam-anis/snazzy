from django.contrib import admin

from .models import Item, ItemVariant, OrderItem, Order

admin.site.register(Item)
admin.site.register(ItemVariant)
admin.site.register(OrderItem)
admin.site.register(Order)	