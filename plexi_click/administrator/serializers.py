from rest_framework import serializers
from api.models import (
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
    User,
    SubcategoryModel
)

class CategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(max_length=100, required=True)
    category_image = serializers.ImageField(required=True)
    class Meta:
        model = CategoryModel
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.category_name', read_only=True)

    class Meta:
        model = ProductModel
        fields = '__all__'

class VariantSerializer(serializers.ModelSerializer):
    product = serializers.CharField()
    color = serializers.CharField()
    size = serializers.CharField()
    thickness = serializers.CharField()
    subcategory = serializers.CharField()
    class Meta:
        model = VariantModel
        fields = '__all__'

class VariantUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantModel
        fields = '__all__'
    def validate_subcategory(self, value):
        if value == '':
            return None
        return value

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactModel
        fields = '__all__'

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = '__all__'

class OrderItemSerializer(serializers.Serializer):
    product_name = serializers.CharField()
    quantity = serializers.IntegerField()
    subcategory = serializers.CharField()
    color = serializers.CharField()
    size = serializers.CharField()
    thickness = serializers.CharField()
    price = serializers.CharField()
    total = serializers.CharField()

class OrderBillingAddressSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    house_no_street_name = serializers.CharField()
    apartment = serializers.CharField()
    town_or_city = serializers.CharField()
    post_code_zip = serializers.CharField()
    email = serializers.EmailField()
    governorates_name = serializers.CharField()
    governorates_amount = serializers.CharField()
    phone_no = serializers.CharField()

class OrderShippingAddressSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    house_no_street_name = serializers.CharField()
    apartment = serializers.CharField()
    town_or_city = serializers.CharField()
    post_code_zip = serializers.CharField()
    company_name = serializers.CharField()

class OrderDetailedSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    order_date = serializers.CharField()
    order_status = serializers.CharField()
    sub_total = serializers.CharField()
    order_total = serializers.CharField()
    payment_status = serializers.CharField()
    deliverd_at = serializers.CharField()
    notes = serializers.CharField()
    order_items = OrderItemSerializer(many=True)
    billing_address = OrderBillingAddressSerializer()
    shipping_address = OrderShippingAddressSerializer()

class ReviewSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.product_name', read_only=True)
    class Meta:
        model = ReviewsModel
        fields = '__all__'

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorModel
        fields = '__all__'

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SizeModel
        fields = '__all__'

class ThicknessSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThicknessModel
        fields = '__all__'

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubcategoryModel
        fields = '__all__'