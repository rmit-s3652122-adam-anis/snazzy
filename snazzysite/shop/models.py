from django.db import models

class ProductStyle(models.Model):
	product_style 		= models.CharField(max_length=100, blank=False, null=False)

	def __str__(self):
		return self.product_style

class ProductType(models.Model):
	product_type		= models.CharField(max_length=100, blank=False, null=False) 

	def __str__(self):
		return self.product_type

class Product(models.Model):
	name 	= models.CharField(max_length=100, blank=False, null=False)
	desc 	= models.TextField()	
	styleID = models.ForeignKey(ProductStyle, on_delete=models.CASCADE)
	typeID 	= models.ForeignKey(ProductType, on_delete=models.CASCADE)

	def __str__(self):
		return self.name

class ProductVariant(models.Model):
	XS 	= "Extra Small"
	S 	= "Small"
	M 	= "Medium"
	L 	= "Large"
	XL 	= "Extra Large"
	XXL = "Extra Extra Large"

	SIZE_CHOICES = (
		(XS, "Extra Small"),
		(S, "Small"),
		(M, "Medium"),
		(L, "Large"),
		(XL, "Extra Large"),
		(XXL, "Extra Extra Large"),
	)

	FEM = "Female"
	MAL = "Male"
	UNI = "Unisex"

	GENDER_CHOICES = (
		(FEM, "Female"),
		(MAL, "Male"),
		(UNI, "Unisex"),

	)

	color 		= models.CharField(max_length=100, blank=False, null=False)
	size 		= models.CharField(max_length=100, choices=SIZE_CHOICES, blank=False, null=False)
	gender 		= models.CharField(max_length=100, choices=GENDER_CHOICES, blank=False, null=False)
	quantity 	= models.PositiveIntegerField(blank=False, null=False)
	price 		= models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False)
	product		= models.ForeignKey(Product, on_delete=models.CASCADE)

	def __str__(self):
		return self.product.name

def product_images_path(instance, filename):
	return 'product_images/{0}/{1}'.format(instance.product.id, filename)

class ProductImage(models.Model):
	product 	= models.ForeignKey(Product, on_delete=models.CASCADE)
	images 		= models.ImageField(upload_to=product_images_path)

	def __str__(self):
		return self.product.name


class OrderProduct(models.Model):
	quantity 	= models.PositiveIntegerField(blank=False, null=False)
	products	= models.ForeignKey(ProductVariant, on_delete=models.CASCADE)

	def __str__(self):
		return self.id


class Order(models.Model):
	STD = "Standard Delivery"
	EXP = "Express Delivery"

	DEL_METHOD_CHOICES = (	
		(STD, "Standard Delivery"),
		(EXP, "Express Delivery"),
	)

	HOLD 		= "On Hold"
	OTW 		= "Delivering"
	DELIVERED 	= "Delivered"

	DEL_STATUS_CHOICES = (
		(HOLD, "On Hold"),
		(OTW, "Delivering"),
		(DELIVERED, "Delivered"),
	)

	CC = "Credit Card"
	PP = "PayPal"

	PAY_METHOD_CHOICES = (
		(CC, "Credit Card"),
		(PP, "PayPal"),

	)

	ref_no 			= models.CharField(max_length=100, blank=False, null=False)
	ordered_date 	= models.DateTimeField(blank=False, null=False)
	delivery_method = models.CharField(max_length=100, choices=DEL_METHOD_CHOICES, blank=False, null=False)
	delivery_status = models.CharField(max_length=100, choices=DEL_STATUS_CHOICES, blank=False, null=False)
	payment_method 	= models.CharField(max_length=100, choices=PAY_METHOD_CHOICES, blank=False, null=False)
	payment_status 	= models.BooleanField(default=False)
	total_price 	= models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False)
	products		= models.ManyToManyField(OrderProduct)

	def __str__(self):
		return self.ref_no
