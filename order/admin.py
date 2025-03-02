from django.contrib import admin
from .models import FoodItem, Order

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'available')
    list_filter = ('available',)
    search_fields = ('name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer__username',)
    ordering = ('-created_at',)
