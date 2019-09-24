from django import forms
from django.forms.models import inlineformset_factory
from django.forms.models import modelformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, Row, HTML, ButtonHolder, Submit
from .custom_layout_object import Formset

from .models import (
    Product,
    ProductImage,
    ProductVariant,
    OrderProduct,
    Order
)

import re

"""ADD NEW PRODUCT FORMS"""
class ProductVariantForm(forms.ModelForm):

    class Meta:
        model = ProductVariant
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        formtag_prefix = re.sub('-[0-9]+$', '', kwargs.get('prefix', ''))

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Field('size'),
                Field('color'),
                Field('quantity'),
                Field('DELETE'),
                css_class='formset_row-{}'.format(formtag_prefix)
            )
        )

ProductVariantFormSet = inlineformset_factory(
    Product, ProductVariant,
    form=ProductVariantForm,
    fields=['size', 'color', 'quantity'],
    min_num=1,
    validate_min=True,
    extra=0,
    can_delete=True
)

class ProductImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')
    
    class Meta:
        model = ProductImage 
        fields = ('image', )

    def __init__(self, *args, **kwargs):
        super(ProductImageForm, self).__init__(*args, **kwargs) 

        formtag_prefix = re.sub('-[0-9]+$', '', kwargs.get('prefix', ''))
        
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Field('image'),
                Field('DELETE'),
                css_class='formset_row-{}'.format(formtag_prefix)
            )
        )  

ProductImageFormSet = inlineformset_factory(
    Product, ProductImage,
    form=ProductImageForm,
    fields=['image'],
    min_num=1,
    validate_min=True,
    extra=0, 
    can_delete=True
    )

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = ['supplier', 'created_at', 'updated_at', 'slug']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(
                Field('product_style'),
                Field('product_type'),
                Field('gender'),
                Field('name'),
                Field('description'),
                Fieldset(
                    'Add variants',
                    Formset('variants')
                ),
                HTML("<br>"),
                Fieldset(
                    'Add images',
                    Formset('images')
                ),
                HTML("<br>"),
                Field('price'),
                ButtonHolder(Submit('submit', 'save')),
            )
        )

"""ADD PRODUCT TO CART FORM"""
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