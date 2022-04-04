from django.urls import path
from .views import (CartListView,AddToCartView,
                    ReduceItemFromCartView,RemoveItemFromCartView,
                    IncreaseQuantityView,CheckoutView)

urlpatterns = [
    path("",CartListView.as_view(),name="url_cartList"),
    path("add-to-cart/<str:product_slug>",AddToCartView.as_view(),name="url_addToCart"),
    path("reduce-cart-item/<unique_id>",ReduceItemFromCartView.as_view(),name="url_reduceItemFromCart"),
    path("remove-item/<unique_id>",RemoveItemFromCartView.as_view(),name="url_removeItemFromCart"),
    path("increase/<unique_id>",IncreaseQuantityView.as_view(),name="url_increaseQuantity"),
    path("checkout/",CheckoutView.as_view(),name="url_checkout")
]