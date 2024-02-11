from rest_framework import serializers
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
    User
)

class CategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(max_length=100, required=True)
    category_image = serializers.ImageField(required=True)
    class Meta:
        model = CategoryModel
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=CategoryModel.objects.all(), required=True)
    product_name = serializers.CharField(max_length=100, required=True)
    product_desc = serializers.CharField(required=True)
    product_image = serializers.ImageField(required=True)
    is_featured = serializers.BooleanField(required=True)
    price_range = serializers.CharField(read_only=True)
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

class ColorSerializer(serializers.Serializer):
    color_name = serializers.CharField()
    variant_count = serializers.IntegerField()

class ContactSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, required=True)
    email = serializers.EmailField(max_length=200, required=True)
    message = serializers.CharField(max_length=500, required=True)

    class Meta:
        model = ContactModel
        fields = '__all__'

class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=200, required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value
    
class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField(max_length=200, required=True)
    password = serializers.CharField(write_only=True, required=True)
    remember_me = serializers.BooleanField(required=False)

class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistModel
        fields = '__all__'

class WishListGetSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    variant_id = serializers.IntegerField(required=False)
    product_id = serializers.IntegerField(required=False)
    product_image = serializers.ImageField(required=False)
    product_name = serializers.CharField(required=False)
    subcategory = serializers.CharField(required=False)
    color = serializers.CharField(required=False)
    size = serializers.CharField(required=False)
    thickness = serializers.CharField(required=False)
    price = serializers.CharField(required=False)
    added_date = serializers.CharField(required=False)
    stock = serializers.IntegerField(required=False)

class UserDetailsSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    class Meta:
        model = User
        fields = ['id','first_name','last_name','username','email']

class UserPasswordSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)

    def validate_current_password(self, value):
        user = self.instance 
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")

        return value

    def validate(self, data):
        current_password = data.get('current_password')
        new_password = data.get('new_password')

        if current_password == new_password:
            raise serializers.ValidationError("New password must be different from the current password.")

        return data

    class Meta:
        model = User
        fields = ['current_password', 'new_password']

class GovernoratesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GovernoratesModel
        fields = '__all__'

class BillingAddressSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=100, required=True)
    last_name = serializers.CharField(max_length=100, required=True)
    house_no_street_name =serializers.CharField(max_length=250, required=True)
    apartment = serializers.CharField(max_length=150, required=False)
    town_or_city = serializers.CharField(max_length=200, required=True)
    post_code_zip = serializers.CharField(max_length=15, required=True)
    phone_no = serializers.IntegerField(required=True)
    email = serializers.EmailField(max_length=100, required=True)
    governorates = serializers.PrimaryKeyRelatedField(queryset=GovernoratesModel.objects.all(), required=True)
    governorates_name = serializers.CharField(source='governorates.governorates_name', required=False)
    governorates_amount = serializers.CharField(source='governorates.governorates_amount', required=False)
    class Meta:
        model = BillingAddressModel
        fields = '__all__'

class ShippingAddressSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=100, required=True)
    last_name = serializers.CharField(max_length=100, required=True)
    company_name = serializers.CharField(max_length=150, required=False)
    house_no_street_name =serializers.CharField(max_length=250, required=True)
    apartment = serializers.CharField(max_length=150, required=False)
    town_or_city = serializers.CharField(max_length=200, required=True)
    post_code_zip = serializers.CharField(max_length=15, required=True)
    class Meta:
        model = ShippingAddressModel
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    variant = serializers.PrimaryKeyRelatedField(queryset=VariantModel.objects.all(), required=True)
    quantity = serializers.IntegerField(required=True)

    class Meta:
        model = CartModel
        fields = ['user','variant','quantity']
    
class CartGetSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    variant_id = serializers.IntegerField()
    variant_image = serializers.ImageField()
    product_name = serializers.CharField()
    subcategory = serializers.CharField()
    color = serializers.CharField()
    size = serializers.CharField()
    thickness = serializers.CharField()
    price = serializers.CharField()
    stock = serializers.CharField()
    quantity = serializers.IntegerField()
    sub_total = serializers.CharField()

class OrderPostSerializer(serializers.ModelSerializer):
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=3, required=True)
    notes = serializers.CharField(max_length=300, required=False)
    class Meta:
        model = OrderModel
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    created_at = serializers.DateTimeField(format="%B %d, %Y", required=False)
    order_status = serializers.CharField(required=False)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=3, required=True)
    class Meta:
        model = OrderModel
        fields = ['id','created_at','order_status','total_amount']

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
    product = serializers.PrimaryKeyRelatedField(queryset=ProductModel.objects.all(), required=True)
    name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    rating = serializers.IntegerField(required=True)
    review = serializers.CharField(required=True)
    class Meta:
        model = ReviewsModel
        fields = '__all__'

class ReviewGetSerializer(serializers.Serializer):
    name = serializers.CharField()
    rating = serializers.IntegerField()
    review = serializers.CharField()
    status = serializers.CharField()
