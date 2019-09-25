from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify
from datetime import timedelta
from users.models import Profile, Address

class ProductStyle(models.Model):
	description = models.CharField(max_length=100, blank=False, null=False)

	def __str__(self):
		return self.description

class ProductType(models.Model):
	description	= models.CharField(max_length=100, blank=False, null=False) 

	def __str__(self):
		return self.description

class Product(models.Model):

	FEM = "FEM"
	MAL = "MAL"
	UNI = "UNI"

	GENDER_CHOICES = (
		(FEM, "Female"),
		(MAL, "Male"),
		(UNI, "Unisex"),
	)

	name 			= models.CharField(max_length=100, blank=False, null=False)
	description 	= models.TextField()
	gender 			= models.CharField(max_length=3, choices=GENDER_CHOICES, default=UNI, blank=False, null=False)
	price 			= models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False)	
	product_style 	= models.ForeignKey(ProductStyle, on_delete=models.SET_NULL, null=True)
	product_type 	= models.ForeignKey(ProductType, on_delete=models.SET_NULL, null=True)
	created_at		= models.DateTimeField(editable=False)
	updated_at 		= models.DateTimeField(null=True)
	slug 			= models.SlugField(unique=True)
	supplier 		= models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.pk:
			self.created_at = timezone.now()
		self.updated_at = timezone.now()
		self.slug = slugify(self.name)
		return super(Product, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('product-detail', kwargs={'slug': self.slug}) # return full string path to product-detail

	def get_add_to_cart_url(self):
		return reverse('product-add-cart', kwargs={
			'slug': self.slug
		})

	def get_remove_from_cart_url(self):
		return reverse('product-remove-cart', kwargs={
			'slug': self.slug
		})

	def is_new(self):

		start_date = self.created_at.date()
		end_date = start_date + timedelta(days=7)
		if end_date > timezone.now().date():
			return True
		return False	

class ProductVariant(models.Model):
	XS 	= "XS"
	S 	= "S"
	M 	= "M"
	L 	= "L"
	XL 	= "XL"
	XXL = "XXL"

	SIZE_CHOICES = (
		(XS, "Extra Small"),
		(S, "Small"),
		(M, "Medium"),
		(L, "Large"),
		(XL, "Extra Large"),
		(XXL, "Extra Extra Large"),
	)

	# FEM = "FEM"
	# MAL = "MAL"
	# UNI = "UNI"

	# GENDER_CHOICES = (
	# 	(FEM, "Female"),
	# 	(MAL, "Male"),
	# 	(UNI, "Unisex"),
	# )

	product		= models.ForeignKey(Product, on_delete=models.CASCADE, related_name="has_variants")
	color 		= models.CharField(max_length=50, blank=False, null=False)
	size 		= models.CharField(max_length=4, choices=SIZE_CHOICES, default=M, blank=False, null=False)
	# gender 		= models.CharField(max_length=3, choices=GENDER_CHOICES, default=UNI, blank=False, null=False)
	quantity 	= models.PositiveIntegerField(blank=False, null=False)
	

	def __str__(self):
		return f'{self.product.name} {self.pk}'

	def get_description(self):
		readable = str(self.color) + " Size " + str(self.size)
		return readable	

def product_images_path(instance, filename):
	return 'product_images/{0}/{1}'.format(instance.product.id, filename) # file will be uploaded to MEDIA_ROOT/product_<id>/<filename>

class ProductImage(models.Model):
	product 	= models.ForeignKey(Product, on_delete=models.CASCADE, related_name="has_images")
	imagefile 	= models.ImageField(upload_to=product_images_path)

	def __str__(self):
		return f'{self.product} image {self.id}'


class OrderProduct(models.Model):
	buyer 			= models.ForeignKey(User, on_delete=models.CASCADE)
	ordered			= models.BooleanField(default=False)
	quantity 		= models.PositiveIntegerField(default = 0, blank=False, null=False)
	product_variant	= models.ForeignKey(ProductVariant, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.pk)

	def get_total_item_price(self):
		return self.quantity * self.product_variant.product.price


class Order(models.Model):
	# STD = "STD"
	# EXP = "EXD"

	# DEL_METHOD_CHOICES = (	
	# 	(STD, "Standard Delivery"),
	# 	(EXP, "Express Delivery"),
	# )

	# CC = "CC"
	# PP = "PP"

	# PAY_METHOD_CHOICES = (
	# 	(CC, "Credit Card"),
	# 	(PP, "PayPal"),
	# )

	buyer 			= models.ForeignKey(User, on_delete=models.CASCADE)
	order_products	= models.ManyToManyField(OrderProduct)
	start_date		= models.DateTimeField(auto_now_add=True)
	ordered_date 	= models.DateTimeField(blank=True, null=True)
	ordered			= models.BooleanField(default=False)
	shipping_address = models.ForeignKey(
		Address, 
		related_name='shipping_address', 
		on_delete=models.SET_NULL,
		blank=True,
		null=True
	)
	billing_address = models.ForeignKey(
		Address, 
		related_name='billing_address', 
		on_delete=models.SET_NULL,
		blank=True,
		null=True
	)
	# payment 		= models.ForeignKey(
    #     'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    # coupon 		= models.ForeignKey(
    #     'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    # being_delivered = models.BooleanField(default=False)
    # received 		= models.BooleanField(default=False)
    # refund_requested = models.BooleanField(default=False)
    # refund_granted = models.BooleanField(default=False)
	# delivery_method = models.CharField(max_length=3, choices=DEL_METHOD_CHOICES, default=STD, blank=True, null=True)
	# ref_no 		= models.CharField(max_length=20, blank=True, null=True)
	# final_price 	= models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False)	

	def __str__(self):
		return f'{self.buyer.username} {self.pk}'

	def get_total(self):
		total = 0
		for order_product in self.order_products.all():
			total += order_product.get_total_item_price()
		return total		

