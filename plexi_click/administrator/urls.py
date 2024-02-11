from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryView.as_view(), name='admin-category-view'),
    path('categories/<int:category_id>/', views.CategoryUpdateView.as_view(), name='category-detail'),

    path('product/<int:product_id>/', views.ProductUpdateView.as_view(), name='product-update-view'),
    path('products/', views.ProductView.as_view(), name='product-post-view'),
    path('product/delete/<product_name>/', views.ProductDeleteView.as_view(), name='product-delete'),

    path('variants/<int:product_id>/', views.VariantView.as_view(), name='variant-api'),
    path('variant/<int:variant_id>/', views.VariantUpdateView.as_view(), name='variant-update-view'),
    path('variants/', views.VariantPostView.as_view(), name='variant-post-view'),
    path('warning_stock/', views.WarningStockView.as_view(), name='warning-stock'),

    path('users/', views.UsersView.as_view(), name='all-users'),
    path('user/<int:user_id>/', views.UpdateUserView.as_view(), name='update-user'),

    path('orders/', views.OrderView.as_view(), name='all-orders'),
    path('order/<int:order_id>', views.OrderDetailedView.as_view(), name='order-detail-view'),
    path('contactus/', views.ContactView.as_view(), name='cotact-messages'),
    path('contact/<int:contact_id>/', views.ContactDetailsView.as_view(), name='cotact-messages-details'),

    path('reviews/<int:product_id>/', views.ReviewView.as_view(), name='review-view'),
    path('review/<int:review_id>/', views.ReviewUpdateView.as_view(), name='review-update'),

    path('colors/', views.ColorView.as_view(), name='colors'),
    path('sizes/', views.SizeView.as_view(), name='sizes'),
    path('thickness/', views.ThicknessView.as_view(), name='thickness'),
    path('subcategory/', views.SubcategoryView.as_view(), name='subcategory'),

    path('color/delete/<int:color_id>/', views.ColorDeleteView.as_view(), name='colors'),
    path('size/delete/<int:size_id>/', views.SizeDeleteView.as_view(), name='sizes'),
    path('thickness/delete/<int:thickness_id>/', views.ThicknessDeleteView.as_view(), name='thickness'),
    path('subcategory/delete/<int:subcategory_id>/', views.SubcategoryDeleteView.as_view(), name='subcategory')
]