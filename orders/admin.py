from django.contrib import admin
from .models import OrderProductModel,OrderModel


class OrderProductInline(admin.TabularInline):
    model = OrderProductModel
    extra = 0

@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display        = ["user","order_number","order_total","status","is_ordered"]
    list_display_links  = ["user","order_number"]
    inlines             = [OrderProductInline]

    class Meta:
        model = OrderModel


@admin.register(OrderProductModel)
class OrderProductAdmin(admin.ModelAdmin):
    list_display       = ["user","order","product","quantity","created_add"]
    list_display_links = ["user","order"]
    list_filter        = ["order","user"]
    class Meta:
        model = OrderProductModel







