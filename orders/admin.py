from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_title', 'author', 'paid']
    list_filter = ['created']
    inlines = [OrderItemInline]
