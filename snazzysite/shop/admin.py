from django.contrib import admin

from .models import *

admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(OrderProduct)
admin.site.register(Order)	
admin.site.register(ProductStyle)	
admin.site.register(ProductType)	
admin.site.register(ProductImage)	
admin.site.register(Payment)
admin.site.register(Rating)	