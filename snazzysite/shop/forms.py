from django import forms
from .models import (
    Product,
    ProductVariant,
    OrderProduct,
    Order
)

# class AddToCartForm(forms.ModelForm):

#     variant = forms.ChoiceField(choices=[])
#     quantity = forms.IntegerField(min_value=1, initial=1 )
    

#     def __init__(self, *args, **kwargs):
#         product = kwargs.pop('product_option', [])
#         # product = product_choice
#         super(AddToCartForm, self).__init__(**kwargs)
#         if product:       
#             product_object = ProductVariant.objects.filter(product=product)
#             VARIANT_CHOICES = []
#             for variant in product_object:
#                 actual_val = variant.pk
#                 readable = str(variant.color) + " Size " + str(variant.size) + " - " + str(variant.quantity) + " left"
#                 VARIANT_CHOICES.append((actual_val, readable))

#             self.fields['variant'].choices = VARIANT_CHOICES

#     class Meta:
#         model = OrderProduct
#         fields = ('variant', 'quantity')

class AddToCartForm(forms.Form):

    variant = forms.ChoiceField(choices=[])
    quantity = forms.IntegerField(min_value=1, initial=1 )
    

    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product_option', [])
        super(AddToCartForm, self).__init__(**kwargs)
        
        if product:       
            product_object = ProductVariant.objects.filter(product=product)
            VARIANT_CHOICES = []
            for variant in product_object:
                actual_val = variant.pk
                readable = str(variant.color) + " Size " + str(variant.size) + " - " + str(variant.quantity) + " left"
                VARIANT_CHOICES.append((actual_val, readable))

            self.fields['variant'].choices = VARIANT_CHOICES