from django.contrib import admin
from .models import Girl, Image, City, Region, Service, Review
from parler.admin import TranslatableAdmin


class ImageInline(admin.StackedInline):
    model = Image


@admin.register(Girl)
class GirlAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'region', 'status', 'rate']
    list_filter = ['updated', 'created']
    search_fields = ['name']
    inlines = [ImageInline]


class RegionInline(admin.TabularInline):
    model = Region
    prepopulated_fields = {'slug': ('name',)}


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}
    inlines =[RegionInline]


@admin.register(Service)
class ServiceAdmin(TranslatableAdmin):
    list_display = ['name', 'slug']
    # prepopulated_fields = {'slug': ('name',)}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['created']
