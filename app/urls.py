from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import OrderCreateAPIView, OrderGetAPIView, UserRegistrationAPIView, IceCreamViewSet, PaymentConfirmView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('login/', obtain_auth_token, name='api_token_auth'),
    path('icecreams/', IceCreamViewSet.as_view({'get': 'list', 'post': 'create'}), name='icecream-list'),
    path('icecreams/<int:pk>/', IceCreamViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='icecream-detail'),
    path('orders/', OrderGetAPIView.as_view(), name='order-list'),
    path('orders/<int:order_id>/', OrderGetAPIView.as_view(), name='order-detail'),
    path('order/', OrderCreateAPIView.as_view(), name='order-create'),
    path('order/confirm/', PaymentConfirmView.as_view(), name='order-confirm'),
]