from django.contrib import admin
from .models import (
    CategoryModel,
    ProductModel,
    ColorModel,
    SizeModel,
    ThicknessModel,
    VariantModel,
    ReviewsModel,
    GovernoratesModel,
    ShippingAddressModel,
    BillingAddressModel,
    CartModel,
    WishlistModel,
    OrderModel,
    OrderItemModel,
    PaymentModel,
    ContactModel,
    SubcategoryModel
)

for model in [
    CategoryModel,
    ProductModel,
    ColorModel,
    SizeModel,
    ThicknessModel,
    VariantModel,
    ReviewsModel,
    GovernoratesModel,
    ShippingAddressModel,
    BillingAddressModel,
    CartModel,
    WishlistModel,
    OrderModel,
    OrderItemModel,
    PaymentModel,
    ContactModel,
    SubcategoryModel
]:
    admin.site.register(model)
