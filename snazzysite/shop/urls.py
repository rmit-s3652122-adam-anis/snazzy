from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeListView.as_view(), name='shop-home'),
    path('product/<slug>/', ProductDetailView.as_view(), name='product-detail'),
    # path('add-to-cart/<slug>/', add_to_cart, name='product-add-cart'),
    path('about/', about, name='shop-about')
]