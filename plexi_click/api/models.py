from django.db import models
from colorfield.fields import ColorField
from django.contrib.auth.models import User

ORDER_STATUS_CHOICES = [
    ('processing', 'Processing'),
    ('ready for dispatch', 'Ready for Dispatch'),
    ('dispatched', 'Dispatched'),
    ('delivered', 'Delivered'),
    ('cancelled', 'Cancelled'),
]

REVIEW_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('hide', 'Hide')
]

class CategoryModel(models.Model):
    category_name = models.CharField(max_length=100,null=True)
    category_image = models.ImageField(null=True,upload_to='category_images')

    def __str__(self):
        return self.category_name

class ProductModel(models.Model):
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, null=True)
    product_name = models.CharField(max_length=100,null=True, unique=True)
    product_desc = models.TextField(null=True)
    product_image = models.ImageField(null=True,upload_to='product_images')
    is_featured = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name

class ColorModel(models.Model):
    color_name = models.CharField(max_length=100,null=True, unique=True)

    def __str__(self):
        return self.color_name

class SizeModel(models.Model):
    size = models.CharField(max_length=50,null=True)

    def __str__(self):
        return self.size

class ThicknessModel(models.Model):
    thickness = models.CharField(max_length=50,null=True)

    def __str__(self):
        return self.thickness
    
class SubcategoryModel(models.Model):
    subcategory = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.subcategory
    
class VariantModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, null=True)
    color = models.ForeignKey(ColorModel, on_delete=models.PROTECT, null=True)
    size = models.ForeignKey(SizeModel, on_delete=models.PROTECT, null=True)
    thickness = models.ForeignKey(ThicknessModel, on_delete=models.PROTECT, null=True)
    subcategory = models.ForeignKey(SubcategoryModel, on_delete=models.SET_NULL, null=True, blank=True)
    variant_image = models.ImageField(null=True,upload_to='variant_images')
    product_price = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    stock = models.IntegerField(null=True)
    reorder_level = models.IntegerField(null=True)

    def __str__(self):
        return self.product.product_name

class ReviewsModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(null=True, max_length=100)
    email = models.EmailField(null=True)
    rating = models.IntegerField(null=True)
    review = models.TextField(null=True, max_length=350)
    review_status = models.CharField(max_length=20, choices=REVIEW_STATUS_CHOICES, default='pending')

class GovernoratesModel(models.Model):
    governorates_name = models.CharField(max_length=50, null=True)
    governorates_amount = models.DecimalField(max_digits=10, decimal_places=3, null=True)

    def __str__(self):
        return self.governorates_name

class BillingAddressModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    house_no_street_name = models.CharField(max_length=100 , null=True)
    apartment = models.CharField(max_length=200, null=True)
    town_or_city = models.CharField(max_length=200, null=True)
    post_code_zip = models.CharField(max_length=11, null=True)
    phone_no = models.IntegerField(null=True)
    email = models.EmailField(null=True)
    governorates = models.ForeignKey(GovernoratesModel,on_delete=models.PROTECT, null=True)

class ShippingAddressModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    company_name = models.CharField(max_length=100 , null=True)
    house_no_street_name = models.CharField(max_length=100 , null=True)
    apartment = models.CharField(max_length=200, null=True)
    town_or_city = models.CharField(max_length=200, null=True)
    post_code_zip = models.CharField(max_length=11, null=True)

class CartModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    variant = models.ForeignKey(VariantModel, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

class WishlistModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, null=True)
    variant = models.ForeignKey(VariantModel, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

class OrderModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(null=True, blank=True)
    payment_status = models.CharField(max_length=20, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='processing')
    billing_email = models.EmailField(max_length=100, null=True, blank=True)
    billing_first_name = models.CharField(max_length=200, null=True, blank=True)
    billing_last_name = models.CharField(max_length=200, null=True, blank=True)
    billing_house_no = models.CharField(max_length=200, null=True, blank=True)
    billing_apartment = models.CharField(max_length=200, null=True, blank=True)
    billing_town = models.CharField(max_length=200, null=True, blank=True)
    billing_post_code_zip = models.CharField(max_length=200, null=True, blank=True)
    billing_phone_no = models.CharField(max_length=200, null=True, blank=True)
    billing_governorates_name = models.CharField(max_length=200, null=True, blank=True)
    billing_governorates_amount = models.CharField(max_length=200, null=True, blank=True)
    shipping_first_name = models.CharField(max_length=200, null=True, blank=True)
    shipping_last_name = models.CharField(max_length=200, null=True, blank=True)
    shipping_house_no = models.CharField(max_length=200, null=True, blank=True)
    shipping_apartment = models.CharField(max_length=200, null=True, blank=True)
    shipping_town = models.CharField(max_length=200, null=True, blank=True)
    shipping_post_code_zip = models.CharField(max_length=200, null=True, blank=True)
    shipping_company_name = models.CharField(max_length=200, null=True, blank=True)
    deliverd_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

class OrderItemModel(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, null=True)
    product_name = models.CharField(max_length=200, null=True, blank=True)
    subcategory = models.CharField(max_length=200, null=True, blank=True)
    color = models.CharField(max_length=200, null=True, blank=True)
    size = models.CharField(max_length=200, null=True, blank=True)
    thickness = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.IntegerField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    image = models.CharField(max_length=400, null=True, blank=True)

class PaymentModel(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    txn_order_id = models.CharField(max_length=100, null=True)
    txn_pay_id = models.CharField(max_length=100, null=True)
    bank_txn_id = models.CharField(max_length=100, null=True)
    txn_status = models.CharField(max_length=100, null=True)
    txn_amount = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    txn_type = models.CharField(max_length=100, null=True)
    gateway_name = models.CharField(max_length=100, null=True)
    bank_name = models.CharField(max_length=100, null=True)
    mid = models.IntegerField(null=True)
    payment_mode = models.CharField(max_length=100, null=True)
    txn_date = models.DateTimeField(auto_now_add=True)

class ContactModel(models.Model):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=200, null=True)
    message = models.TextField(max_length=500, null=True)

    def __str__(self):
        return self.name