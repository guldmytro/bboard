from django.contrib import admin
from .models import Order, OrderItem, TariffOrderItem, TariffOrder


class OrderItemInline(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_title', 'author', 'paid']
    list_filter = ['created']
    inlines = [OrderItemInline]


class TariffOrderItemInline(admin.TabularInline):
    model = TariffOrderItem


@admin.register(TariffOrder)
class TariffOrderAdmin(admin.ModelAdmin):
    list_display = ['order_title', 'author', 'paid']
    list_filter = ['created']
    inlines = [TariffOrderItemInline]
