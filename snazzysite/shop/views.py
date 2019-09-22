from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View, FormView
from django.views.generic.edit import FormMixin
from .forms import AddToCartForm
from django.utils import timezone


from .models import *

# Create your views here.

# def home(request):
#     return render(request, 'shop/home.html')

class HomeListView(ListView):
    model = Product
    template_name = 'shop/home.html'
    context_object_name = 'products'
    ordering = ['-created_at']
    paginate_by = 10

class ProductDetailView(FormMixin, DetailView):
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
            order = order_qs[0]
            # add new order product into existing order object
            # if order.order_products.filter(product_variant__id = p_variant.id).exists():
            if created:
                # order product object existed in order, add-on to order-product quantity
                new_order_product.quantity += post_quantity
                new_order_product.save()
                messages.info(self.request, "This product quantity was updated")
            else:
                # new order product to be added into order
                order.order_products.add(new_order_product)
                messages.info(self.request, "This product was added to your cart")
        else:
            # create new order and add new order product into order
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
        # return reverse('product_detail', kwargs={'slug': self.object.slug})
        return redirect('product-detail', kwargs={
            'slug': self.object.slug
        })         

def about(request):
    return render(request, 'shop/about.html', {'title': 'About'})