from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import View
from store.models import ProductModel,ProductVariationModel
from .models import CartModel,CartItemModel
from django.contrib.auth.mixins import LoginRequiredMixin

def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart


class CartListView(View):
    http_method_names = ["get"]

    def get(self,request,total=0,quantity=0,cart_items=None):
        grand_total=0
        tax=0
        try:
            if request.user.is_authenticated:
                cart_items = CartItemModel.objects.filter(user=request.user,is_active=True)
            else:
                cart       = CartModel.objects.get(cart_id=_cart_id(request))
                cart_items = CartItemModel.objects.filter(cart=cart,is_active=True)
            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)
                quantity+=cart_item.quantity
            tax=(2*total)/100
            grand_total=total+tax
        except:
            pass
        ctx={
            "total":total,
            "quantity":quantity,
            "cart_items":cart_items,
            "tax":tax,
            "grand_total":grand_total,
        }

        return render(request,"cart/cart.html",ctx)


class AddToCartView(View):
    http_method_names = ["post"]
    variations = list()

    def check_is_variation(self):
        for item in self.request.POST:
            key   = item
            value = self.request.POST.get(key)
            if key=="csrfmiddlewaretoken":
                continue
            variation = get_object_or_404(ProductVariationModel,product=self.get_product(),
                              variation_category__iexact=key,
                              variation_value__iexact=value)
            self.variations.append(variation)

        return True

    def get_product(self):
        return get_object_or_404(ProductModel,slug=self.kwargs.get("product_slug"))

    def get_cart(self):
        if self.request.user.is_authenticated:
            try:
                cart = CartModel.objects.get(user=self.request.user)
            except:
                cart = CartModel.objects.create(user=self.request.user,cart_id=_cart_id(self.request))
        else:
            try:
                cart = CartModel.objects.get(cart_id=_cart_id(self.request))
            except CartModel.DoesNotExist:
                cart = CartModel.objects.create(cart_id=_cart_id(self.request))
            cart.save()
        return cart

    def get_cart_item(self):
        if self.request.user.is_authenticated:
            return CartItemModel.objects.filter(product=self.get_product(), user=self.request.user).order_by("-id")[0]
        return CartItemModel.objects.filter(product=self.get_product(), cart=self.get_cart()).order_by("-id")[::1][0]

    def is_any_product_with_same_variations(self):
        product     = self.get_product()
        cart        = self.get_cart()
        cart_items  = CartItemModel.objects.filter(product=product,cart=cart) #sepetteki aynı ürünlerin hepsi

        ozellikler = list()
        for urun in cart_items:
            ozellikler.append(list(urun.variations.all().order_by("id")))

        if self.variations in ozellikler:
            self.variations.clear()
            return True # Sepette aynı özelliklere sahip bir ürün var
        else:
            return False # sepette aynı özelliklere sahip bir ürün yok

    def add_variations_to_cart(self):
        cart_item = self.get_cart_item()
        if len(self.variations) > 0:
            cart_item.variations.clear()

            for item in self.variations:
                cart_item.variations.add(item)
            cart_item.save()
            self.variations.clear()

    def create_cart_item(self):
        if self.request.user.is_authenticated:
            cart_item = CartItemModel.objects.create(product=self.get_product(), quantity=1, cart=self.get_cart(),user=self.request.user)
        else:
            cart_item = CartItemModel.objects.create(product=self.get_product(), quantity=1, cart=self.get_cart())

        cart_item.save()

        return cart_item

    def increase_quantitiy(self):
        cart_item = self.get_cart_item()
        cart_item.quantity += 1
        cart_item.save()

    def post(self,request,product_slug):
        if self.check_is_variation():
            if self.is_any_product_with_same_variations():
                #self.increase_quantitiy()   # eğer aynı ürün varsa adeti arttırıyoruz
                pass
            else:                           # Sepette aynı ürün yoksa
                self.create_cart_item()
            self.add_variations_to_cart()
            return redirect("url_cartList")


class BaseRemoveCartView(View):
    http_method_names = ["get"]

    def get_cart(self):
        if not self.request.user.is_authenticated:
            cart = CartModel.objects.get(cart_id=_cart_id(self.request))
        else:
            cart = CartModel.objects.get(user=self.request.user)
        return cart


class ReduceItemFromCartView(BaseRemoveCartView):
    def get(self,request,unique_id):
        cart      = self.get_cart()
        try:
            cart_item = CartItemModel.objects.get(unique_id=unique_id,user=request.user)
        except:
            cart_item = CartItemModel.objects.get(unique_id=unique_id,cart=cart)

        if cart_item.quantity>1:
            cart_item.quantity-=1
            cart_item.save()
        else:
            cart_item.delete()
        return redirect("url_cartList")


class RemoveItemFromCartView(BaseRemoveCartView):
    def get(self,request,unique_id):
        cart = self.get_cart()
        try:
            cart_item = CartItemModel.objects.get(unique_id=unique_id,user=request.user)
        except:
            cart_item = CartItemModel.objects.get(unique_id=unique_id,cart=cart)
        cart_item.delete()
        return redirect("url_cartList")


class IncreaseQuantityView(View):
    http_method_names = ["get"]

    def get_cart_item(self):

        return get_object_or_404(CartItemModel,unique_id=self.kwargs.get("unique_id"))

    def get(self,request,unique_id):
        cart_item = self.get_cart_item()
        cart_item.quantity += 1
        cart_item.save()
        return redirect("url_cartList")


class CheckoutView(LoginRequiredMixin,View):
    http_method_names = ["get","post"]
    def get(self,request,total=0,quantity=0,cart_items=None):
        grand_total = 0
        tax = 0
        try:
            cart_items = CartItemModel.objects.filter(user=self.request.user, is_active=True)
            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (2 * total) / 100
            grand_total = total + tax
        except Exception as e:
            pass
        ctx = {
            "total": total,
            "quantity": quantity,
            "cart_items": cart_items,
            "tax": tax,
            "grand_total": grand_total,
        }

        return render(request,"cart/checkout.html",ctx)




