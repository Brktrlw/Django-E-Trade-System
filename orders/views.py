import datetime
import uuid
from django.contrib import messages
from django.core.mail import EmailMessage
from django.db import transaction
from django.template.loader import render_to_string
from django.views.generic import View,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from cart.models import CartItemModel
from django.shortcuts import redirect, render
from store.models import ProductModel
from .forms import OrderForm
from .models import OrderModel, OrderProductModel


class PlaceOrderView(LoginRequiredMixin,View):
    http_method_names = ["get","post"]

    def get_cart_items(self):
        return CartItemModel.objects.filter(user=self.request.user)

    def get_price_info(self):
        total = 0
        quantity = 0
        cart_items = self.get_cart_items()
        for item in cart_items:
            total += (item.product.price * item.quantity)
            quantity += item.quantity
        tax = (2 * total) / 100
        grand_total = total + tax
        return {"grand_total":grand_total,"tax":tax,"total":total}

    def get_date(self):
        year  = int(datetime.date.today().strftime("%Y"))
        day   = int(datetime.date.today().strftime("%d"))
        month = int(datetime.date.today().strftime("%m"))
        date  = datetime.date(year=year,month=month,day=day)
        current_date = date.strftime("%Y%m%d")
        return current_date

    def get(self,request):
        user = request.user
        self.cart_items = CartItemModel.objects.filter(user=user)
        cart_count = self.cart_items.count()
        if cart_count <= 0:
            return redirect("url_store")

        return redirect("url_store")

    def post(self,request):
        form = OrderForm(request.POST)
        if form.is_valid():
            order_data = form.save(commit=False)
            order_data.order_total  = self.get_price_info().get("grand_total")
            order_data.tax          = self.get_price_info().get("tax")
            order_data.ip           = self.request.META.get("REMOTE_ADDR")
            order_data.user         = self.request.user
            order_data.created_date = self.get_date()
            order_data.order_number =  str(self.get_date()) + "-"+ str(uuid.uuid4())
            form.save()
            order = OrderModel.objects.get(user=self.request.user,is_ordered=False,order_number=order_data.order_number)
            ctx={
                "order":order,
                "cart_items":self.get_cart_items(),
                "grand_total":self.get_price_info().get("grand_total"),
                "tax":self.get_price_info().get("tax"),
                "total":self.get_price_info().get("total"),
            }

            return render(request,"orders/payments.html",ctx)
        else:
            messages.error(request,"Bir sorun oluştu")
            return redirect("url_checkout")


class PaymentView(LoginRequiredMixin,View):
    http_method_names = ["get","post"]

    def get(self,request):
        return render(request,"orders/payments.html")

    def cartItemsToOrderItems(self):
        cart_items   = CartItemModel.objects.filter(user=self.request.user)
        order_number = self.get_post_data().get("order_number")
        order        = OrderModel.objects.filter(order_number=order_number)[0]

        for item in cart_items:
            cart_item = CartItemModel.objects.get(id=item.id)
            variation = cart_item.variations.all()

            order_item = OrderProductModel.objects.create(
                order_id      = order.id,
                user          = self.request.user,
                product       = item.product,
                quantity      = item.quantity,
                product_price = item.product.price,
                ordered       = True,
            )
            order_item = OrderProductModel.objects.get(id=order_item.id)
            order_item.variation.set(variation)
            order_item.save()

            # stoktan azaltma
            product = ProductModel.objects.get(id=item.product.id)
            product.stock -= item.quantity
            product.save()
        CartItemModel.objects.filter(user=self.request.user).delete()

    def send_mail_to_user(self):
        try:
            with transaction.atomic():
                mail_subject = "Siparişiniz İçin Teşekkürler"
                message = render_to_string("orders/order_mail.html", {
                    "user" : self.request.user,
                    "order": self.get_order()
                })
                to_email = self.request.user.email

                send_email = EmailMessage(mail_subject, message, to=[to_email], )
                send_email.send()
        except Exception as e:
            print(e)
            messages.error(self.request, "Bir Sorun Oluştu. Lütfen sonra tekrar deneyiniz.")

    def get_order(self):
        return OrderModel.objects.get(order_number=self.get_post_data().get("order_number"))


    def get_post_data(self):
        card_name    = self.request.POST.get("card_name")
        card_number  = self.request.POST.get("card_number")
        card_exp     = self.request.POST.get("card_exp")
        card_cvv     = self.request.POST.get("card_cvv")
        order_number = self.request.POST.get("order_number")
        return {
            "card_name":card_name,"card_number":card_number,"card_exp":card_exp,"card_cvv":card_cvv,"order_number":order_number
        }

    def get_order_items(self):
        order_items = OrderProductModel.objects.filter(order=self.get_order())
        return order_items

    def post(self,request):
        isPaymentSuccess = True
        if isPaymentSuccess:
            self.cartItemsToOrderItems()
            self.send_mail_to_user()
            order = self.get_order()

            ctx = {
                "order_number":self.get_post_data().get("order_number"),
                "status":order.status,
                "date":order.created_date,
                "order_items":self.get_order_items(),
                "tax":order.tax,
                "total":order.order_total

            }
            return render(request,"orders/order_complete.html",ctx)
        else:
            messages.error(request,"Sipariş işlemi sırasında bir sorun oluştu")
            return render()


class OrderCompleteView(LoginRequiredMixin,TemplateView):
    template_name = "orders/order_complete.html"




