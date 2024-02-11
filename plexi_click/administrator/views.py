from django.shortcuts import render
from api import models
from . import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication 
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.db.models import F

#category
class CategoryView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if request.user.is_staff:
            try:
                categories = models.CategoryModel.objects.all()
                serializer = serializers.CategorySerializer(categories, many=True)
                return Response({"status":"success", "data":serializer.data},status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"status":"error","message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        
    def post(self, request):
        if request.user.is_staff:
            serializer = serializers.CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"Category added"}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        
class CategoryUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def patch(self, request, category_id):
        if request.user.is_staff:
            try:
                category = models.CategoryModel.objects.get(id=category_id)
            except models.CategoryModel.DoesNotExist:
                return Response({"message": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = serializers.CategorySerializer(category, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Category updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN) 
        
    def get(self, request, category_id):
        if request.user.is_staff:
            try:
                categories = models.CategoryModel.objects.get(id=category_id)
                serializer = serializers.CategorySerializer(categories)
                return Response({"status":"success", "data":serializer.data},status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"status":"error","message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        
    def delete(self, request, category_id):
        if request.user.is_staff:
            try:
                category = models.CategoryModel.objects.get(id=category_id)
                category.delete()

                return Response({"status": "success", "message": "category deleted successfully"},
                                status=status.HTTP_200_OK)

            except models.OrderModel.DoesNotExist:
                return Response({"status": "error", "message": "Order not found"},
                                status=status.HTTP_404_NOT_FOUND)

            except Exception as e:
                return Response({"status": "error", "message": str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)

#products      
class ProductView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if request.user.is_staff:
            try:
                products = models.ProductModel.objects.all()
                serializer = serializers.ProductSerializer(products, many=True)
                return Response({"status":"success", "data":serializer.data},status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"status":"error","message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        
    def post(self, request):
        if request.user.is_staff:
            serializer = serializers.ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"Product added"}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        
class ProductUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def patch(self, request, product_id):
        if request.user.is_staff:
            try:
                product = models.ProductModel.objects.get(id=product_id)
            except models.ProductModel.DoesNotExist:
                return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = serializers.ProductSerializer(product, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Product updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        
    def get(self, request, product_id):
        if request.user.is_staff:
            try:
                products = models.ProductModel.objects.get(id=product_id)
                serializer = serializers.ProductSerializer(products, many=True)
                return Response({"status":"success", "data":serializer.data},status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"status":"error","message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        

        
class ProductDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, product_name):
        if request.user.is_staff:
            try:
                product = models.ProductModel.objects.get(product_name=product_name)
                product.delete()

                return Response({"status": "success", "message": "Product deleted successfully"},
                                status=status.HTTP_200_OK)

            except models.ProductModel.DoesNotExist:
                return Response({"status": "error", "message": "Product not found"},
                                status=status.HTTP_404_NOT_FOUND)

            except Exception as e:
                return Response({"status": "error", "message": str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)

# variants   
class VariantView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, product_id):
        if request.user.is_staff:
            try:
                variants = models.VariantModel.objects.filter(product=product_id)
                data=[]
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
                return Response({"status":"success", "data":serializer.data},status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"status":"error","message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        
class VariantPostView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        if request.user.is_staff:
            serializer = serializers.VariantUpdateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"Variant added"}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        
    def get(self, request):
        if request.user.is_staff:
            try:
                variants = models.VariantModel.objects.all()
                serializer = serializers.VariantSerializer(variants, many=True)
                return Response({"status":"success", "data":serializer.data},status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"status":"error","message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        
class VariantUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def patch(self, request, variant_id):
        if request.user.is_staff:
            try:
                variant = models.VariantModel.objects.get(id=variant_id)
            except models.VariantModel.DoesNotExist:
                return Response({"message": "Variant not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = serializers.VariantUpdateSerializer(variant, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Variant updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        
    def get(self, request, variant_id):
        if request.user.is_staff:
            try:
                variants = models.VariantModel.objects.get(id=variant_id)
                serializer = serializers.VariantUpdateSerializer(variants)
                return Response({"status":"success", "data":serializer.data},status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"status":"error","message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        
    def delete(self, request, variant_id):
        if request.user.is_staff:
            try:
                variant = models.VariantModel.objects.get(id=variant_id)
                variant.delete()

                return Response({"status": "success", "message": "Variant deleted successfully"},
                                status=status.HTTP_200_OK)

            except models.VariantModel.DoesNotExist:
                return Response({"status": "error", "message": "Variant not found"},
                                status=status.HTTP_404_NOT_FOUND)

            except Exception as e:
                return Response({"status": "error", "message": str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        
class WarningStockView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if request.user.is_staff:
            try:
                variants = models.VariantModel.objects.filter(stock__lte=F('reorder_level'))
                data=[]
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
                return Response({"status":"success", "data":serializer.data},status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"status":"error","message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)

#users
class UsersView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if request.user.is_staff:
            try:
                users = models.User.objects.all()
                serializer = serializers.UsersSerializer(users, many=True)
                return Response({"status":"success", "data":serializer.data},status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"status":"error","message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)

class UpdateUserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id):
        if request.user.is_staff:
            try:
                user = models.User.objects.get(id=user_id)
                serializer = serializers.UsersSerializer(user)
                return Response({"status":"success", "data":serializer.data},status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"status":"error","message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        
    def patch(self, request, user_id):
        if request.user.is_staff:
            try:
                user = models.User.objects.get(id=user_id)
            except models.User.DoesNotExist:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = serializers.UsersSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        
#orders
class OrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if request.user.is_staff:
            try:
                orders = models.OrderModel.objects.all()
                serializer = serializers.OrderSerializer(orders, many=True)
                return Response({"status":"success", "data":serializer.data},status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"status":"error","message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)

# to view order details
class OrderDetailedView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        if request.user.is_staff:
            try:
                order = get_object_or_404(models.OrderModel, id=order_id)
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
                    "username": order.user.username,
                    "order_date": order.created_at,
                    "order_status": order.order_status,
                    "sub_total": sub_total,
                    "order_total": order.total_amount,
                    "payment_status": order.payment_status,
                    "deliverd_at": order.deliverd_at,
                    "notes": order.notes,
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
        else:
            return Response({"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        
    def patch(self, request, order_id):
        if request.user.is_staff:
            try:
                order = models.OrderModel.objects.get(id = order_id)
                new_status =  request.data.get('order_status')

                if new_status is not None:
                    order.order_status = new_status

                    if new_status.lower() == 'delivered':
                        order.deliverd_at = datetime.now()
                    else:
                        order.deliverd_at = None
                    
                    order.save()

                    return Response({"status": "success", "message": "Order updated successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response({"status": "error", "message": "Status is required in the request data"}, status=status.HTTP_400_BAD_REQUEST)

            except models.OrderModel.DoesNotExist:
                return Response({"status": "error", "message": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        
    def delete(self, request, order_id):
        if request.user.is_staff:
            try:
                order = models.OrderModel.objects.get(id=order_id)
                order.delete()

                return Response({"status": "success", "message": "Order deleted successfully"},
                                status=status.HTTP_200_OK)

            except models.OrderModel.DoesNotExist:
                return Response({"status": "error", "message": "Order not found"},
                                status=status.HTTP_404_NOT_FOUND)

            except Exception as e:
                return Response({"status": "error", "message": str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)

# messages
class ContactView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if request.user.is_staff:
            try:
                messages = models.ContactModel.objects.all()
                serializer = serializers.ContactSerializer(messages, many=True)
                return Response({"status":"success", "data":serializer.data},status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"status":"error","message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        
class ContactDetailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, contact_id):
        if request.user.is_staff:
            try:
                contact = models.ContactModel.objects.get(id=contact_id)
                serializer = serializers.ContactSerializer(contact)
                return Response({"status":"success", "data":serializer.data},status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"status":"error","message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        
    def delete(self, request, contact_id):
        if request.user.is_staff:
            try:
                contact = models.ContactModel.objects.get(id=contact_id)
                contact.delete()

                return Response({"status": "success", "message": "Message deleted successfully"}, status=status.HTTP_200_OK)

            except models.ContactModel.DoesNotExist:
                return Response({"status": "error", "message": "Message not found"}, status=status.HTTP_404_NOT_FOUND)

            except Exception as e:
                return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        
class ReviewView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]       
    def get(self, request, product_id):
        if request.user.is_staff:
            try:
                reviews = models.ReviewsModel.objects.filter(product=product_id)
                serializer = serializers.ReviewSerializer(reviews, many=True)
                return Response({"status":"success", "data":serializer.data},status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"status":"error","message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        
class ReviewUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, review_id):
        if request.user.is_staff:
            try:
                review = models.ReviewsModel.objects.get(id=review_id)
                serializer = serializers.ReviewSerializer(review)
                return Response({"status":"success", "data":serializer.data},status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"status":"error","message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        
    def patch(self, request, review_id):
        if request.user.is_staff:
            try:
                review = models.ReviewsModel.objects.get(id = review_id)
                new_status =  request.data.get('review_status')

                if new_status is not None:
                    review.review_status = new_status
                    
                    review.save()

                    return Response({"status": "success", "message": "Review updated successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response({"status": "error", "message": "Status is required in the request data"}, status=status.HTTP_400_BAD_REQUEST)

            except models.OrderModel.DoesNotExist:
                return Response({"status": "error", "message": "Review not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        
    def delete(self, request, review_id):
        if request.user.is_staff:
            try:
                review = models.ReviewsModel.objects.get(id=review_id)
                review.delete()

                return Response({"status": "success", "message": "Review deleted successfully"}, status=status.HTTP_200_OK)

            except models.ReviewsModel.DoesNotExist:
                return Response({"status": "error", "message": "Review not found"}, status=status.HTTP_404_NOT_FOUND)

            except Exception as e:
                return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        
class ColorView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]       
    def get(self, request):
        if request.user.is_staff:
            try:
                colors = models.ColorModel.objects.all()
                serializer = serializers.ColorSerializer(colors, many=True)
                return Response({"status":"success", "data":serializer.data},status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"status":"error","message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        
    def post(self, request):
        if request.user.is_staff:
            serializer = serializers.ColorSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"color added"}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        
class ColorDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated] 
    def delete(self, request, color_id):
        if request.user.is_staff:
            try:
                color = models.ColorModel.objects.get(id=color_id)
                color.delete()

                return Response({"status": "success", "message": "Color deleted successfully"}, status=status.HTTP_200_OK)

            except models.ColorModel.DoesNotExist:
                return Response({"status": "error", "message": "Color not found"}, status=status.HTTP_404_NOT_FOUND)

            except Exception as e:
                return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        
class SizeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]       
    def get(self, request):
        if request.user.is_staff:
            try:
                sizes = models.SizeModel.objects.all()
                serializer = serializers.SizeSerializer(sizes, many=True)
                return Response({"status":"success", "data":serializer.data},status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"status":"error","message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        
    def post(self, request):
        if request.user.is_staff:
            serializer = serializers.SizeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"size added"}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        
class SizeDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated] 
    def delete(self, request, size_id):
        if request.user.is_staff:
            try:
                size = models.SizeModel.objects.get(id=size_id)
                size.delete()

                return Response({"status": "success", "message": "Size deleted successfully"}, status=status.HTTP_200_OK)

            except models.SizeModel.DoesNotExist:
                return Response({"status": "error", "message": "Size not found"}, status=status.HTTP_404_NOT_FOUND)

            except Exception as e:
                return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        
class ThicknessView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]       
    def get(self, request):
        if request.user.is_staff:
            try:
                thickness = models.ThicknessModel.objects.all()
                serializer = serializers.ThicknessSerializer(thickness, many=True)
                return Response({"status":"success", "data":serializer.data},status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"status":"error","message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        
    def post(self, request):
        if request.user.is_staff:
            serializer = serializers.ThicknessSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"Thickness added"}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        
class ThicknessDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated] 
    def delete(self, request, thickness_id):
        if request.user.is_staff:
            try:
                thickness = models.ThicknessModel.objects.get(id=thickness_id)
                thickness.delete()

                return Response({"status": "success", "message": "Thickness deleted successfully"}, status=status.HTTP_200_OK)

            except models.ThicknessModel.DoesNotExist:
                return Response({"status": "error", "message": "Thickness not found"}, status=status.HTTP_404_NOT_FOUND)

            except Exception as e:
                return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        
class SubcategoryView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]       
    def get(self, request):
        if request.user.is_staff:
            try:
                subcategory = models.SubcategoryModel.objects.all()
                serializer = serializers.SubcategorySerializer(subcategory, many=True)
                return Response({"status":"success", "data":serializer.data},status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"status":"error","message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        
    def post(self, request):
        if request.user.is_staff:
            serializer = serializers.SubcategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"Subcategory added"}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        
class SubcategoryDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated] 
    def delete(self, request, subcategory_id):
        if request.user.is_staff:
            try:
                subcategory = models.SubcategoryModel.objects.get(id=subcategory_id)
                subcategory.delete()

                return Response({"status": "success", "message": "Subcategory deleted successfully"}, status=status.HTTP_200_OK)

            except models.SubcategoryModel.DoesNotExist:
                return Response({"status": "error", "message": "Subcategory not found"}, status=status.HTTP_404_NOT_FOUND)

            except Exception as e:
                return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)