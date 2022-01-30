from django.contrib import admin
from .models import Rate, Category, Toss


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Toss)
class TossAdmin(admin.ModelAdmin):
    list_display = ['quantity', 'price']
