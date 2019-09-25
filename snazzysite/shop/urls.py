from django.urls import path
from .views import *

urlpatterns = [
    # home view
    path('', HomeListView.as_view(), name='shop-home'),

    # create new product view function
    path('product/new/', ProductCreateView.as_view(), name='product-create'),

    # product detail view function
    path('product/<slug>/', ProductDetailView.as_view(), name='product-detail'),

    # order summary view functions
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('add-to-cart/<variant_id>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<variant_id>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<variant_id>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),

    # about page     
    path('about/', about, name='shop-about'),

    # checkout page
    path('checkout/', CheckoutView.as_view(), name='checkout'),

    # payment page
    path('payment/<option>/', PaymentView.as_view(), name='payment'),

]