from .models import CartModel,CartItemModel
from .views import _cart_id


def cart_counter(request):
    try:
        cart        = CartModel.objects.filter(cart_id=_cart_id(request))
        if request.user.is_authenticated:
            cart_items = CartItemModel.objects.filter(user=request.user)
        else:
            cart_items  = CartItemModel.objects.filter(cart=cart[:1])
        cart_count  = cart_items.count()

    except Exception as e:
        cart_count=0
    return dict(cart_count=cart_count)





