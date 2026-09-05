from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderLogistics

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'session_token', 'status', 'user']

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'quantity', 'cart', 'variation']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'status', 'total_amount', 'payment_tx_id', 'shipment_tracking', 'cart', 'user']

class OrderLogisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderLogistics
        fields = ['id', 'shipping_address', 'billing_address', 'order']
