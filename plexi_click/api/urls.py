from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path('',views.server),
    path('category/', views.CategoryView.as_view(), name='category-api'),
    path('category/<int:category_id>/', views.CategorySortView.as_view(), name='category-based-sorting-api'),
    path('products/', views.ProductView.as_view(), name='product-listing-api'),
    path('product/<product_name>/', views.ProductDetailedView.as_view(), name='product-details-api'),
    path('variants/<product_name>/', views.VariantView.as_view(), name='product-based-variants-api'),
    path('variant/<int:variant_id>/', views.VariantDetailedView.as_view(), name='varinat-detailed-view'),
    path('products/filter/', views.ProductFilteringView.as_view(), name='products-filter-api'),    
    path('governorates/', views.GovernoratesView.as_view(), name='governorates-api'),
    path('contactus/', views.ContactView.as_view(), name='contact-us-api'),

    path('token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    path('account/user/registration/', views.UserRegistrationView.as_view(), name='user-registration-api'),
    path('account/user/logout/', views.LogoutView.as_view(), name='user-logout'),
    path('account/user/login/', views.LoginView.as_view(), name='user-login-api'),

    path('user/wishlist/', views.WishListView.as_view(), name='wishlist-api'),
    path('user/wishlist/delete/', views.WishlistDeleteView.as_view(), name='wishlist-delete-api'),

    path('account/user/details/', views.UserDetailsView.as_view(), name='user-details-api'),
    path('account/user/details/password/', views.PasswordChangeView.as_view(), name='user-password-updating-api'),
    path('account/user/details/billing-address/', views.BillingAddressView.as_view(), name='billing-address-api'),
    path('account/user/details/shipping-address/', views.ShippingAddressView.as_view(), name='shipping-address-api'),

    path('user/cart/', views.CartAndCheckoutView.as_view(), name='cart-api'),
    path('user/cart/delete/<int:cart_id>/', views.CartDeleteView.as_view(), name='cart-delete-api'),
    path('user/place-order/', views.PlaceOrderView.as_view(), name='place-order-api'),
    path('user/orders/', views.OrderView.as_view(), name='order-view-api'),
    path('user/orders/<int:order_id>/', views.OrderDetailedView.as_view(), name='order-view-api'),
    path('user/orders/track-order/', views.TrackOrderView.as_view(), name='track-order-api'),
    
    path('products/review/', views.ReviewView.as_view(), name='review-api'),
    path('product/review/user/', views.ReviewUserView.as_view(), name='review-user-api'),

    path('initiate_payment/<int:order_id>/', views.initiate_payment, name='initiate_payment'),
]