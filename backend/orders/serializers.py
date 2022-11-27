from rest_framework import serializers
from orders.models import Order, OrderLine
from django.core.validators import MinValueValidator, validate_slug
from donuts.serializers import DonutShortSerializer


class OrderLineSerializer(serializers.ModelSerializer):
    donut = DonutShortSerializer()

    class Meta:
        model = OrderLine
        fields = [
            'donut',
            'quantity',
            'price',
        ]


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')
    lines = OrderLineSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'customer_name',
            'status',
            'price',
            'lines',
        ]


class CreateOrderLineSerializer(serializers.Serializer):
    donut_code = serializers.CharField(
        max_length=50,
        validators=[validate_slug],
    )
    quantity = serializers.IntegerField(
        default=1,
        validators=[MinValueValidator(1)],
    )


class CreateOrderSerializer(serializers.Serializer):
    customer_name = serializers.CharField(max_length=1024)
    donuts = CreateOrderLineSerializer(many=True)
