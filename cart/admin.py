from django.contrib import admin
from .models import CartModel,CartItemModel

class CartItemInline(admin.TabularInline):
    model = CartItemModel
    extra = 0


@admin.register(CartModel)
class CartAdmin(admin.ModelAdmin):
    list_display        = ["user","cart_id","date_added"]
    list_display_links  = ["user","cart_id"]
    search_fields       = ["cart_id"]
    list_filter         = ["date_added"]
    inlines             = [CartItemInline]

    class Meta:
        model=CartModel

@admin.register(CartItemModel)
class CartItemAdmin(admin.ModelAdmin):
    list_display       = ["user","cart","product","quantity"]
    list_display_links = ["user","cart"]
    search_fields      = ["product"]
    list_filter        = ["user"]
    list_editable      = ("quantity",)

    class Meta:
        model = CartItemModel




