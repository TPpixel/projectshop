from rest_framework import serializers
from .models import Category, Manufacturer, Product, Basket, BasketItem, Order, OrderItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class BasketItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketItem
        fields = '__all__'


class BasketSerializer(serializers.ModelSerializer):
    позиции = BasketItemSerializer(many=True, read_only=True, source='basketitem_set')
    общая_стоимость = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Basket
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    позиции = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
