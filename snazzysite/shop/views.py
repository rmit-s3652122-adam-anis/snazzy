from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.views.generic.edit import FormMixin
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import (
    LoginRequiredMixin, 
    UserPassesTestMixin
    )     
from django.views.generic import (
    CreateView,
    ListView, 
    DetailView, 
    View, 
    FormView,
    )
from django.utils import timezone

from .forms import *
from .models import *

# Create your views here.

class HomeListView(ListView):
    model = Product
    template_name = 'shop/home.html'
    context_object_name = 'products'
    ordering = ['-created_at']
    paginate_by = 10

class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    Create View to users to add new products 
    """
    model = Product
    template_name = 'shop/product_form.html'
    form_class =  ProductForm
    sucess_url = None

    def get_context_data(self, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['variants'] = ProductVariantFormSet(self.request.POST)
            context['images'] = ProductImageFormSet(self.request.POST, self.request.FILES)
        else:
            context['variants'] = ProductVariantFormSet()
            context['images'] = ProductImageFormSet()
        return context

    # def post(self, request, *args, **kwargs):
    #     self.object = None
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     variant_form = ProductVariantFormSet(self.request.POST)
    #     print(variant_form.is_valid())
    #     image_form = ProductImageFormSet(self.request.POST, self.request.FILES)
    #     print(image_form.is_valid())
    #     print(image_form.cleaned_data)
    #     if form.is_valid and variant_form.is_valid and image_form.is_valid():
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)

    def form_valid(self, form):
        print('in form valid for update')
        context = self.get_context_data()
        variants = context['variants']
        images = context['images']
        print(images.cleaned_data)
        with transaction.atomic():
            # create new product object
            form.instance.supplier = self.request.user
            self.object = form.save()
            print("product ok")
            if variants.is_valid():
                # create new variants objects
                variants.instance = self.object
                variants.save()
                print("variants ok")
            if images.is_valid():
                # create new images objects
                for image in images.cleaned_data:
                    if image:
                        print(image)
                        imagefile = image['imagefile']
                        product = self.object
                        product_image = ProductImage(product=product, imagefile=imagefile)
                        product_image.save()
                print("images ok")
            messages.info(self.request, "Successfully added new product")    
            return super(ProductCreateView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(ProductCreateView, self).form_invalid(form)

    def get_success_url(self):
        return reverse('shop-home')            
                
class ProductDetailView(FormMixin, DetailView):
    """
    Display product detail and add new product to order/cart
    """
    model = Product
    context_object_name = 'product'
    template_name = "shop/product_detail.html"
    form_class = AddToCartForm

    def get_form_kwargs(self):
        kwargs = super(ProductDetailView, self).get_form_kwargs()
        kwargs.update({'product_option': self.get_object()})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        # context['form'] = AddToCartForm(product_choice=self.get_object())
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            print("INVALID")
            return self.form_invalid(form)   

    def form_valid(self, form):
        post_id = form.cleaned_data['variant']
        post_quantity = form.cleaned_data['quantity']
        # get product variant object
        p_variant = get_object_or_404(ProductVariant, pk=post_id)
        # get/create order product object
        new_order_product, created = OrderProduct.objects.get_or_create(
            product_variant = p_variant,
            buyer = self.request.user,
            ordered=False,
            defaults={'quantity': post_quantity}
        )
        # check if order object exists
        order_qs = Order.objects.filter(buyer=self.request.user, ordered=False)
        if order_qs.exists():
            print("order exists")
            order = order_qs[0]
            # add new order product into existing order object
            if order.order_products.filter(product_variant__id = p_variant.id).exists():
                print("order product exists")
                # order product object existed in order, add-on to order-product quantity
                new_order_product.quantity += post_quantity
                new_order_product.save()
                messages.info(self.request, "This product quantity was updated")
            else:
                print("new order product")
                # new order product to be added into order
                order.order_products.add(new_order_product)
                messages.info(self.request, "This product was added to your cart")
        else:
            # create new order and add new order product into order
            print("new order")
            ordered_date = timezone.now()
            order = Order.objects.create(
                buyer=self.request.user, 
                ordered_date=ordered_date
            )
            order.order_products.add(new_order_product)
            messages.info(self.request, "New order created, order product was added to your cart")
        return super(ProductDetailView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(ProductDetailView, self).form_invalid(form)    

    def get_success_url(self):
        return reverse('product-detail', kwargs={
            'slug': self.object.slug
        })


@login_required
def remove_from_cart(request, variant_id):
    """
    From order_summary view
    Remove a product variant from cart
    """
    # item = get_object_or_404(Item, slug=slug)
    product_variant = get_object_or_404(ProductVariant, id=variant_id)
    order_qs = Order.objects.filter(
        buyer=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.order_products.filter(product_variant__id=product_variant.id).exists():
            order_product = OrderProduct.objects.filter(
                product_variant=product_variant,
                buyer=request.user,
                ordered=False
            )[0]
            order.order_products.remove(order_product)
            messages.info(request, "This item was removed from your cart.")
    return redirect("order-summary")
    #     else:
    #         messages.info(request, "This item was not in your cart")
    #         return redirect("product-detail", slug=slug)
    # else:
    #     messages.info(request, "You do not have an active order")
    #     return redirect("product-detail", slug=slug)                 


@login_required
def remove_single_item_from_cart(request, variant_id):
    """
    From order_summary view
    Remove a single quantity of a product variant from cart
    """
    product_variant = get_object_or_404(ProductVariant, id=variant_id)
    order_qs = Order.objects.filter(
        buyer=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.order_products.filter(product_variant__id=product_variant.id).exists():
            order_product = OrderProduct.objects.filter(
                product_variant=product_variant,
                buyer=request.user,
                ordered=False
            )[0]
            if order_product.quantity > 1:
                order_product.quantity -= 1
                order_product.save()
            else:
                order.order_products.remove(order_product)
            messages.info(request, "This item quantity was updated.")
    return redirect("order-summary")
    #     else:
    #         messages.info(request, "This item was not in your cart")
    #         return redirect("core:product", slug=slug)
    # else:
    #     messages.info(request, "You do not have an active order")
    #     return redirect("core:product", slug=slug)


@login_required
def add_to_cart(request, variant_id):
    """
    From order_summary view
    Add a quantity of a product variant to cart
    """
    product_variant = get_object_or_404(ProductVariant, id=variant_id)
    order_product, created = OrderProduct.objects.get_or_create(
        product_variant=product_variant,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(buyer=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.order_products.filter(product_variant__id=product_variant.id).exists():
            order_product.quantity += 1
            order_product.save()
            messages.info(request, "This item quantity was updated.")
        else:
            order.order_products.add(order_product)
            messages.info(request, "This item was added to your cart.")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            buyer=request.user, ordered_date=ordered_date)
        order.products.add(order_product)
        messages.info(request, "This item was added to your cart.")
    return redirect("order-summary")    


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(buyer=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'shop/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")

def about(request):
    return render(request, 'shop/about.html', {'title': 'About'})