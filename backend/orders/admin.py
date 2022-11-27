from django.contrib import admin
from orders.models import Order, OrderLine


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'price')
    list_display = ('id', 'customer_name', 'status')


@admin.register(OrderLine)
class OrderLineAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'price')
    list_display = ('id', 'order', 'donut', 'quantity')
