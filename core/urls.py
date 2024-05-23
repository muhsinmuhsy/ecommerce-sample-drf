from django.urls import path
from .views import LoginView, LogoutView, AddToCartView, ViewCartView, CheckoutView, OrderConfirmationView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('cart/add/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', ViewCartView.as_view(), name='view_cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order/confirmation/<int:order_id>/', OrderConfirmationView.as_view(), name='order_confirmation'),
    
]
