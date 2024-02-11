from django.shortcuts import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum,Min,Max
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication 
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import filters
from django.contrib.auth.models import AnonymousUser
from datetime import timedelta
from django.db import transaction
import razorpay
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from . import models
from . import serializers

def server(request):
    return HttpResponse("server running")

# View all categories
class CategoryView(APIView):
    def get(self, request):
        try:
            categories = models.CategoryModel.objects.all()
            serializer = serializers.CategorySerializer(categories, many=True)
            return Response({"status":"success", "data":serializer.data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":"error","message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# sort products based on categories
class CategorySortView(APIView):
    def get(self, request, category_id):
        try:
            products = models.ProductModel.objects.filter(category_id = category_id)
            if not products:
                return Response({"status": "error", "message": "No products found with given category id"}, status=status.HTTP_404_NOT_FOUND)
            serializer = serializers.ProductSerializer(products, many=True)
            return Response({"status":"success", "data":serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":"error","message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# view all products
class ProductView(APIView):
    def get(self, request):
        try:
            products = models.ProductModel.objects.all()
            serializer = serializers.ProductSerializer(products, many=True)
            return Response({"status":"success","data":serializer.data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":"error","message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# view details of certain product
class ProductDetailedView(APIView):
    def get(self, request, product_name):
        try:
            product = models.ProductModel.objects.get(product_name=product_name)
            category_name = product.category.category_name
            serializer = serializers.ProductSerializer(product)

            serializer_data = serializer.data
            serializer_data['category_name'] = category_name
            return Response({"status":"success", "data":serializer_data}, status=status.HTTP_200_OK) 
        except Exception as e:
            return Response({"status":"error","message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# view variants for a certain product
class VariantView(APIView):
    def get(self, request, product_name):
        try:
            product_id = models.ProductModel.objects.get(product_name = product_name)
            variants = models.VariantModel.objects.filter(product_id = product_id)
            if not variants:
               return Response({"status": "error", "message": "No variant found with given product id"}, status=status.HTTP_404_NOT_FOUND)
            data = []
            for variant in variants:
                data.append({
                    "id": variant.id,
                    "variant_image": variant.variant_image,
                    "product_price": variant.product_price,
                    "sale_price": variant.sale_price,
                    "stock": variant.stock,
                    "product": variant.product.product_name,
                    "subcategory": variant.subcategory.subcategory if variant.subcategory else None,
                    "color": variant.color.color_name,
                    "size": variant.size.size,
                    "thickness": variant.thickness.thickness,
                    "reorder_level": variant.reorder_level,
                })
            serializer = serializers.VariantSerializer(data, many=True)
            return Response({"status":"success","data":serializer.data}, status=status.HTTP_200_OK)     
        except Exception as e:
            return Response({"status":"error","message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class VariantDetailedView(APIView):
    def get(self, request, variant_id):
        try:
            variant = get_object_or_404(models.VariantModel, id=variant_id)
            
            data = {
                "id": variant.id,
                "variant_image": variant.variant_image,
                "product_price": variant.product_price,
                "sale_price": variant.sale_price,
                "stock": variant.stock,
                "product": variant.product.product_name,
                "subcategory": variant.subcategory.subcategory if variant.subcategory else None,
                "color": variant.color.color_name,
                "size": variant.size.size,
                "thickness": variant.thickness.thickness,
                "reorder_level": variant.reorder_level,
            }
            serializer = serializers.VariantSerializer(data)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except models.VariantModel.DoesNotExist:
            return Response({"status": "error", "message": "Variant not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# filtering products
class ProductFilteringView(APIView):
    def get(self, request):
        color_name = request.GET.get('filter_color', None)
        min_price = request.GET.get('min_price', None)
        max_price = request.GET.get('max_price', None)
        category_name = request.GET.get('category_name', None)
        keyword = request.GET.get('keyword', None)

        products_queryset = models.ProductModel.objects.all()

        if category_name:
            category = get_object_or_404(models.CategoryModel, category_name=category_name)
            products_queryset = products_queryset.filter(category=category)

        if color_name:
            color = get_object_or_404(models.ColorModel, color_name=color_name)
            variant_with_color = models.VariantModel.objects.filter(color=color)
            product_ids = variant_with_color.values_list('product_id', flat=True)
            products_queryset = products_queryset.filter(id__in=product_ids)

        if min_price is not None or max_price is not None:
            variant_queryset = models.VariantModel.objects.filter(product_id__in=products_queryset)

            if min_price:
                variant_queryset = variant_queryset.filter(sale_price__gte=min_price)

            if max_price:
                variant_queryset = variant_queryset.filter(sale_price__lte=max_price)

            product_ids = variant_queryset.values_list('product_id', flat=True)

            if not product_ids:
                return Response({"status": "error", "message": "No products match the specified criteria"}, status=status.HTTP_404_NOT_FOUND)
            

            products_queryset = products_queryset.filter(id__in=product_ids)

            if keyword:
                products_queryset = products_queryset.filter(Q(product_name__icontains=keyword) | Q(category__category_name__icontains=keyword))

        if not products_queryset:
            return Response({"status": "error", "message": "No products match the specified criteria"}, status=status.HTTP_404_NOT_FOUND)
        
        price_range = self.calculate_price_range(products_queryset)
        color_count_data = self.calculate_color_count(products_queryset)

        # Serialize the data with the calculated price_range
        serializer = serializers.ProductSerializer(products_queryset, many=True)
        serialized_data = serializer.data
        for data in serialized_data:
            data['price_range'] = price_range[data['id']]
            data['color_count'] = color_count_data[data['id']]

        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    
    def calculate_price_range(self, products_queryset):
        price_ranges = {}
        for product in products_queryset:
            variants = models.VariantModel.objects.filter(product_id=product.id)
            min_price = variants.aggregate(price_min=Min('sale_price'))['price_min']
            max_price = variants.aggregate(price_max=Max('sale_price'))['price_max']
            price_ranges[product.id] = f"{min_price} د.ك  {max_price} - د.ك"
        return price_ranges
    
    def calculate_color_count(self, products_queryset):
        color_count_data = {}
        for product in products_queryset:
            colors = models.VariantModel.objects.filter(product_id=product.id).values_list('color__color_name', flat=True)
            color_count_data[product.id] = {color: list(colors).count(color) for color in set(colors)}
        return color_count_data


# contact
class ContactView(APIView):
    def post(self, request):
        serializer = serializers.ContactSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Contact information saved successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# user registration
class UserRegistrationView(APIView):
    def post(self, request):
        serializer = serializers.RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            email = data.get('email')
            password = data.get('password')
            username = email.split('@')[0]

            # Check if the email is already in use
            if models.User.objects.filter(email=email).exists():
                return Response({"message": "Email is already in use"}, status=status.HTTP_400_BAD_REQUEST)
            
            original_username = username
            count = 1
            while models.User.objects.filter(username=username).exists():
                username = f"{original_username}_{count}"
                count += 1

            user = models.User(email=email, username=username)
            user.set_password(password)
            user.save()

            billing_address = models.BillingAddressModel(user=user)
            billing_address.email = email
            billing_address.save()

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response_data = {"message": "User Registration completed and logged in", "access_token": access_token,"refresh_token": refresh_token}
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = serializers.LoginSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            username_or_email = data.get('username_or_email')
            password = data.get('password')
            remember_me = data.get("remember_me")

            # Authenticate user
            user = models.User.objects.filter(
                Q(username=username_or_email) | Q(email=username_or_email)
            ).first()

            if user and user.check_password(password):
                refresh = RefreshToken.for_user(user)
                decoded_refresh_token = refresh.payload

                if remember_me:
                    decoded_refresh_token['exp'] = int((refresh.current_time + timedelta(days=30)).timestamp())
                else:
                    decoded_refresh_token['exp'] = int((refresh.current_time + timedelta(days=1)).timestamp())

                # Encode the modified payload back to refresh token
                refresh.payload = decoded_refresh_token
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                response_data = {
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,          
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({"error": "Refresh token is required for logout."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            RefreshToken(refresh_token).blacklist()
            return Response({"message": "Logout successful."},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid refresh token.","message":str(e)},status=status.HTTP_400_BAD_REQUEST)

# api for adding items to wish list and get
class WishListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product')
        variant_id = request.data.get('variant')

        if (product_id is None and variant_id is None) or (product_id is not None and variant_id is not None):
           return Response({"status":"error","message": "Please provide either 'product_id' or 'variant_id', but not both."}, status=status.HTTP_400_BAD_REQUEST)

        existing_item = models.WishlistModel.objects.filter(user=request.user, product_id=product_id, variant_id=variant_id).first()

        if existing_item:
            return Response({"message": "Item already exists in the wishlist."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.WishListSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message": "Item added to the wishlist."}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        try:
            wishlists = models.WishlistModel.objects.filter(user=request.user)
            if not wishlists:
               return Response({"status": "error", "message": "No wishlist data found for this user"}, status=status.HTTP_404_NOT_FOUND)
            data = []
            for wishlist in wishlists:
                if wishlist.variant_id is None:
                    product_id = wishlist.product_id
                    product = models.ProductModel.objects.get(id=product_id)
                    variants = models.VariantModel.objects.filter(product_id=product_id)
                    total_stock = variants.aggregate(total_stock=Sum('stock'))['total_stock']
                    price_range = f"{variants.aggregate(price_min=Min('sale_price'))['price_min']} - {variants.aggregate(price_max=Max('sale_price'))['price_max']}"
                    added_date = wishlist.created_at.strftime("%B %d, %Y")
                    data.append({
                        "id":wishlist.id,
                        "product_id": product.id,
                        "product_image": product.product_image,
                        "product_name": product.product_name,
                        "price": price_range,
                        "added_date":added_date,
                        "stock": total_stock
                    })
                if wishlist.product_id is None:
                    variant_id = wishlist.variant_id
                    variant = models.VariantModel.objects.get(id=variant_id)
                    added_date = wishlist.created_at.strftime("%B %d, %Y")
                    data.append({
                        "id": wishlist.id,
                        "variant_id": variant.id,
                        "product_image": variant.variant_image,
                        "product_name": variant.product.product_name,
                        "subcategory": variant.subcategory.subcategory if variant.subcategory else None,
                        "color": variant.color.color_name,
                        "size": variant.size.size,
                        "thickness": variant.thickness.thickness,
                        "price": variant.sale_price,
                        "added_date":added_date,
                        "stock": variant.stock,
                    })
            serializer = serializers.WishListGetSerializer(data, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# api for deleting wishlist items ( single or multiple )
class WishlistDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        
        item_ids = request.data.get('item_ids', [])
        print(item_ids)
        if not item_ids:
            return Response({"message": "No items selected for deletion."}, status=status.HTTP_400_BAD_REQUEST)
        deleted_item_ids = []
        for item_id in item_ids:
            try:
                wishlist = models.WishlistModel.objects.get(id=item_id)
                if wishlist.user == request.user:
                    wishlist.delete()
                    deleted_item_ids.append(item_id)
            except models.WishlistModel.DoesNotExist:
                return Response({"status":"error", "message":"items does not exists"}, status=status.HTTP_404_NOT_FOUND)
        
        if deleted_item_ids:
            return Response({"status": "success", "message": f"Deleted items with IDs: {', '.join(map(str, deleted_item_ids))}"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "message": "No items were deleted."}, status=status.HTTP_400_BAD_REQUEST)

# user basic details
class UserDetailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        try:
            user_details = models.User.objects.get(id=request.user.id)
            serializer = serializers.UserDetailsSerializer(user_details)

            role = "admin" if user_details.is_staff else "user"

            serialized_data = serializer.data
            serialized_data["role"] = role

            return Response({"status":"success","data":serialized_data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":"error", "message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request):
        
        if models.User.objects.exclude(id=request.user.id).filter(username=request.data.get('username')).exists():
                return Response({"status": "error", "message": "username already existed."}, status=status.HTTP_400_BAD_REQUEST)
        if models.User.objects.exclude(id=request.user.id).filter(email=request.data.get('email')).exists():
                return Response({"status": "error", "message": "email already existed."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user_details = models.User.objects.get(id=request.user.id)
            billing_address = models.BillingAddressModel.objects.get(user=request.user)
            user_serializer = serializers.UserDetailsSerializer(user_details, data=request.data,)
            billing_serializer = serializers.BillingAddressSerializer(billing_address, data=request.data, partial=True)
            if user_serializer.is_valid() and billing_serializer.is_valid():
                user_serializer.save()
                billing_serializer.save()

                return Response({"status": "success", "message": "User details updated."}, status=status.HTTP_200_OK)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# user password updating
class PasswordChangeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user

        serializer = serializers.UserPasswordSerializer(data=request.data, instance=request.user)

        if serializer.is_valid():
            password = serializer.validated_data.get('new_password')
            user.set_password(password)
            user.save()
            return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GovernoratesView(APIView):
    def get(self, request):
        try:
            governorates = models.GovernoratesModel.objects.all()
            serializer = serializers.GovernoratesSerializer(governorates, many=True)
            return Response({"status":"success","data":serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":"error","message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
class BillingAddressView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        
        try: 
            billing_address = models.BillingAddressModel.objects.get(user=request.user)
            serializer = serializers.BillingAddressSerializer(billing_address, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "message": "Billing Address successfully updated."}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status":"error","message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get(self, request):
        
        try:
            billing_address = models.BillingAddressModel.objects.get(user=request.user)
            serializer = serializers.BillingAddressSerializer(billing_address)
            return Response({"status":"success", "data":serializer.data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":"error","message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ShippingAddressView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            shipping_address, created = models.ShippingAddressModel.objects.get_or_create(user=request.user)
            serializer = serializers.ShippingAddressSerializer(shipping_address, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status":"success", "message":"shipping address added successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status":"error","message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get(self, request):
        try:
            shipping_address = models.ShippingAddressModel.objects.get(user=request.user)
            serializer = serializers.ShippingAddressSerializer(shipping_address)
            return Response({"status":"success", "data":serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":"error","message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# cart items managing and checkout view      
class CartAndCheckoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            items = request.data.get('items', [])  # Get the array of items from the request data
            for item in items:
                serializer = serializers.CartSerializer(data=item)
                if serializer.is_valid():
                    variant_id = serializer.validated_data['variant']
                    quantity = serializer.validated_data['quantity']
                    user_cart_item = models.CartModel.objects.filter(user=request.user, variant=variant_id).first()

                    if user_cart_item:
                        # If the variant exists in the cart, update the quantity
                        user_cart_item.quantity += quantity
                        user_cart_item.save()
                    else:
                        # If the variant doesn't exist, create a new entry in the cart
                        serializer.save(user=request.user)

            return Response({"status": "success", "message": "Items added to the cart"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get(self, request):
        try:
            cart_items = models.CartModel.objects.filter(user=request.user)

            if not cart_items:
                return Response({"status":"error","message":"No cart data for this user"}, status=status.HTTP_404_NOT_FOUND)
            data = []
            for item in cart_items:
                variant = models.VariantModel.objects.get(id=item.variant_id)
                sub_total = variant.sale_price * item.quantity
                data.append({
                    "id": item.id,
                    "variant_id": variant.id,
                    "variant_image": variant.variant_image,
                    "product_name": variant.product.product_name,
                    "subcategory": variant.subcategory.subcategory if variant.subcategory else None,
                    "color": variant.color.color_name,
                    "size": variant.size.size,
                    "thickness": variant.thickness.thickness,
                    "price": variant.sale_price,
                    "stock": variant.stock,
                    "quantity": item.quantity,
                    "sub_total": sub_total
                })


            serializer = serializers.CartGetSerializer(data, many=True)
            
           
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":"error","message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CartDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, cart_id):
        try:
            if not cart_id:
                return Response({"status":"error","message":"please provide cart id for deletion"}, status=status.HTTP_400_BAD_REQUEST)
            cart_item = models.CartModel.objects.filter(user=request.user, id=cart_id).first()

            if not cart_item:
                return Response({"status": "error", "message": "No item with given cart id"}, status=status.HTTP_404_NOT_FOUND)

            cart_item.delete()
            return Response({"status": "success", "message": "Item removed from the cart"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# place order managment and store entire info. in order table    
class PlaceOrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = serializers.OrderPostSerializer(data=request.data)
            cart_datas = models.CartModel.objects.filter(user=request.user)
            if not cart_datas:
                return Response({"status":"error","message":"nothing in cart to proceed the order"})
            if serializer.is_valid():
                with transaction.atomic():
                    for cart_data in cart_datas:
                        if cart_data.variant.stock < cart_data.quantity:
                            return Response({"status": "error", "message": "Insufficient stock."}, status=status.HTTP_400_BAD_REQUEST)
                    instance = serializer.save(user=request.user)
                    billing_address = models.BillingAddressModel.objects.get(user=request.user)

                order = models.OrderModel.objects.get(id=instance.id)
            
                order.billing_email = billing_address.email
                order.billing_first_name = billing_address.first_name
                order.billing_last_name = billing_address.last_name
                order.billing_house_no = billing_address.house_no_street_name
                order.billing_apartment = billing_address.apartment
                order.billing_town = billing_address.town_or_city
                order.billing_post_code_zip = billing_address.post_code_zip
                order.billing_phone_no = billing_address.phone_no
                order.billing_governorates_name = billing_address.governorates.governorates_name
                order.billing_governorates_amount = billing_address.governorates.governorates_amount

                shipping_address = models.ShippingAddressModel.objects.filter(user=request.user).first()
                if shipping_address is not None:
                    order.shipping_first_name = shipping_address.first_name
                    order.shipping_last_name = shipping_address.last_name
                    order.shipping_house_no = shipping_address.house_no_street_name
                    order.shipping_apartment = shipping_address.apartment
                    order.shipping_town = shipping_address.town_or_city
                    order.shipping_post_code_zip = shipping_address.post_code_zip
                    order.shipping_company_name = shipping_address.company_name
                
    
                for cart_data in cart_datas:
                    order_item = models.OrderItemModel.objects.create(
                        order=instance,
                        product_name=cart_data.variant.product.product_name,
                        subcategory = cart_data.variant.subcategory.subcategory if cart_data.variant.subcategory else None,
                        color = cart_data.variant.color.color_name,
                        size=cart_data.variant.size.size,
                        thickness=cart_data.variant.thickness.thickness,
                        quantity=cart_data.quantity,
                        price=cart_data.variant.sale_price,
                    )
                    variant = cart_data.variant
                    variant.stock -= cart_data.quantity
                    variant.save()
                
                order.save()
                cart_datas.delete()
                return Response({"status":"success","order_id":order.id}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status":"error","message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# to get lsit of orders      
class OrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            orders = models.OrderModel.objects.filter(user=request.user)
            if not orders:
                return Response({"status":"error","message":"no orders available for this user"}, status=status.HTTP_404_NOT_FOUND)
            serializer = serializers.OrderSerializer(orders, many=True)
            return Response({"status":"success","data":serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":"error","message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# to view order details
class OrderDetailedView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            order = get_object_or_404(models.OrderModel, id=order_id, user=request.user)
            order_items = models.OrderItemModel.objects.filter(order=order)
            order_items_data = []
            for order_item in order_items:
                total = order_item.quantity * order_item.price
                order_items_data.append({
                    "product_name": order_item.product_name,
                    "quantity": order_item.quantity,
                    "subcategory": order_item.subcategory,
                    "color": order_item.color,
                    "size": order_item.size,
                    "thickness": order_item.thickness,
                    "price": order_item.price,
                    "total": total,
                })

            sub_total = sum(item['total'] for item in order_items_data)
            sub_total = "{:.3f}".format(sub_total)

            order_data = {
                "id": order.id,
                "order_date": order.created_at.strftime("%B %d, %Y"),
                "order_status": order.order_status,
                "sub_total": sub_total,
                "order_total": order.total_amount,
                "payment_status": order.payment_status,
                "deliverd_at": order.deliverd_at,
                "notes": order.notes,
                "billing_email": order.billing_email,
                "order_items": order_items_data,
                "billing_address":{
                    "first_name": order.billing_first_name,
                    "last_name": order.billing_last_name,
                    "house_no_street_name": order.billing_house_no,
                    "apartment": order.billing_apartment,
                    "town_or_city": order.billing_town,
                    "post_code_zip": order.billing_post_code_zip,
                    "email": order.billing_email,
                    "governorates_name": order.billing_governorates_name,
                    "governorates_amount": order.billing_governorates_amount,
                    "phone_no": order.billing_phone_no,
                },
                "shipping_address":{
                    "first_name": order.shipping_first_name,
                    "last_name": order.shipping_last_name,
                    "house_no_street_name": order.shipping_house_no,
                    "apartment": order.shipping_apartment,
                    "town_or_city": order.shipping_town,
                    "post_code_zip": order.shipping_post_code_zip,
                    "company_name": order.shipping_company_name,
                }
            }
            serializer = serializers.OrderDetailedSerializer(order_data)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        except models.OrderModel.DoesNotExist:
            return Response({"status": "error", "message": "Order does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# for order tracking
class TrackOrderView(APIView):
    def post(self,request):
        order_id = request.data.get('order_id')
        billing_email = request.data.get('billing_email')
        if not (order_id and billing_email):
            return Response({"status": "error","message":"Order ID and Billing Email are required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            order = get_object_or_404(models.OrderModel, id=order_id, billing_email=billing_email)
            order_items = models.OrderItemModel.objects.filter(order=order)
            order_items_data = []
            for order_item in order_items:
                total = order_item.quantity * order_item.price
                order_items_data.append({
                    "product_name": order_item.product_name,
                    "quantity": order_item.quantity,
                    "subcategory": order_item.subcategory,
                    "color": order_item.color,
                    "size": order_item.size,
                    "thickness": order_item.thickness,
                    "price": order_item.price,
                    "total": total,
                })

            sub_total = sum(item['total'] for item in order_items_data)
            sub_total = "{:.3f}".format(sub_total)

            order_data = {
                "id": order.id,
                "order_date": order.created_at.strftime("%B %d, %Y"),
                "order_status": order.order_status,
                "sub_total": sub_total,
                "order_total": order.total_amount,
                "payment_status": order.payment_status,
                "deliverd_at": order.deliverd_at,
                "notes": order.notes,
                "billing_email": order.billing_email,
                "order_items": order_items_data,
                "billing_address":{
                    "first_name": order.billing_first_name,
                    "last_name": order.billing_last_name,
                    "house_no_street_name": order.billing_house_no,
                    "apartment": order.billing_apartment,
                    "town_or_city": order.billing_town,
                    "post_code_zip": order.billing_post_code_zip,
                    "email": order.billing_email,
                    "governorates_name": order.billing_governorates_name,
                    "governorates_amount": order.billing_governorates_amount,
                    "phone_no": order.billing_phone_no,
                },
                "shipping_address":{
                    "first_name": order.shipping_first_name,
                    "last_name": order.shipping_last_name,
                    "house_no_street_name": order.shipping_house_no,
                    "apartment": order.shipping_apartment,
                    "town_or_city": order.shipping_town,
                    "post_code_zip": order.shipping_post_code_zip,
                    "company_name": order.shipping_company_name,
                }
            }
            serializer = serializers.OrderDetailedSerializer(order_data)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        except models.OrderModel.DoesNotExist:
            return Response({"status": "error", "message": "Order does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# reviews management
class ReviewView(APIView):
    def post(self, request):
        try:
            serializer = serializers.ReviewSerializer(data=request.data)
            if serializer.is_valid():
                if request.user and not isinstance(request.user, AnonymousUser):
                    serializer.save(user=request.user)
                else:
                    serializer.save(user=None) 
                return Response({"status":"success","message":"review saved successfully"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status":"error", "message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get(self, request):
        product_name = request.GET.get("product_name")
        if not product_name:
            return Response({"status":"error","message":"provide a product_id"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            reviews = models.ReviewsModel.objects.filter(review_status='accepted', product_id__product_name=product_name)
            if not reviews:
                return Response({"message":"no reviews availble for this product"}, status=status.HTTP_404_NOT_FOUND)
            review_data = []
            for review in reviews:
                review_data.append({
                    "name": review.name,
                    "rating": review.rating,
                    "review": review.review,
                    "status": review.review_status
                })
            serializer = serializers.ReviewGetSerializer(review_data, many=True)
            return Response({"status":"success","data":serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":"error", "message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# reviews of a logined user
class ReviewUserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        product_id = request.GET.get("product_id")
        if not product_id:
            return Response({"status":"error","message":"provide a product_id"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            reviews = models.ReviewsModel.objects.filter(user=request.user, product_id=product_id)
            if not reviews:
                return Response({"message":"no reviews availble for this product"}, status=status.HTTP_404_NOT_FOUND)
            review_data = []
            for review in reviews:
                review_data.append({
                    "name": review.name,
                    "rating": review.rating,
                    "review": review.review,
                    "status": review.review_status
                })
            serializer = serializers.ReviewGetSerializer(review_data, many=True)
            return Response({"status":"success","data":serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
           return Response({"status":"error", "message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def initiate_payment(request, order_id):
    order = models.OrderModel.objects.get(id=order_id)
    amount = order.total_amount

    client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

    data = client.order.create({
        'amount': int(amount * 1000),
        'currency': 'KWD',
        "receipt": f"order_rcptid_{order_id}"
    })

    payment = models.PaymentModel(order=order, user=request.user, txn_order_id=data["id"], txn_amount=amount, txn_status=data["status"])
    payment.save()

    # return JsonResponse(data)

    return JsonResponse({
        'razorpay_order_id': data['id'],
        'razorpay_amount': data['amount'],
        'razorpay_currency': data['currency'],
    })