from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db import transaction
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.views.generic import View, ListView, DetailView
from django.shortcuts import render , redirect
from django.views.generic import FormView
from cart.models import CartModel, CartItemModel
from cart.views import _cart_id
from orders.models import OrderModel
from .forms import RegisterForm,UserProfileForm
from django.contrib.auth import logout
from .models import UserModel, UserProfileModel
from django.contrib.auth.mixins import LoginRequiredMixin

class EditProfileView(LoginRequiredMixin,FormView):
    template_name = "account/edit_profile.html"
    form_class = UserProfileForm

    def form_valid(self, form):
        user = self.request.user
        userProfileObj= self.get_object()
        user.first_name   = form.cleaned_data.get("first_name")
        user.last_name    = form.cleaned_data.get("last_name")
        user.phone_number = form.cleaned_data.get("phone_number")
        userProfileObj.city          = form.cleaned_data.get("city")
        userProfileObj.clear_address = form.cleaned_data.get("clear_address")
        userProfileObj.address_title = form.cleaned_data.get("address_title")
        user.save()
        userProfileObj.save()
        messages.success(self.request,"Profiliniz başarıyla güncellendi.")
        return redirect("url_editProfile")

    def get_object(self, queryset=None):
        return UserProfileModel.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super(EditProfileView, self).get_context_data(**kwargs)
        userProfileObject = self.get_object()
        ctx["city"]          = userProfileObject.city
        ctx["clear_address"] = userProfileObject.clear_address
        ctx["avatar"]        = userProfileObject.avatar
        ctx["address_title"] = userProfileObject.address_title
        ctx["phone_number"]  = userProfileObject.user.phone_number
        ctx["first_name"]    = userProfileObject.user.first_name
        ctx["last_name"]     = userProfileObject.user.last_name
        return ctx


class RegisterView(FormView):
    template_name = "account/register.html"
    form_class    = RegisterForm

    def is_any_username(self,username):
        return UserModel.objects.filter(username=username).exists()

    def is_any_email(self,email):
        return UserModel.objects.filter(email=email).exists()

    def form_valid(self, form):
        try:
            with transaction.atomic():
                user = form.save(commit=False)

                if self.is_any_username(user.username):
                    messages.error(self.request,"Bu kullanıcı adına sahip başka bir kullanıcı var.")
                    return redirect("url_register")

                elif self.is_any_email(user.email):
                    messages.error(self.request,"Bu mail adresine sahip başka bir kullanıcı var.")
                    return redirect("url_register")

                user.is_active=False
                current_site = get_current_site(self.request)
                mail_subject = "Hesabınızı Aktifleştirin"
                form.save()
                message = render_to_string("account/account_verification.html", {
                    "user" : user,
                    "domain":current_site,
                    "uid":urlsafe_base64_encode(force_bytes(user.id)),
                    "token":default_token_generator.make_token(user)
                })
                to_email = user.email
                send_email = EmailMessage(mail_subject,message,to=[to_email],)
                send_email.send()
                UserProfileModel.objects.create(user=user).save()
                return redirect(f'/user/login/?command=verification&email={user.email}')

        except Exception as e:
            messages.error(self.request,"Bir Sorun Oluştu")
            return redirect("url_register")


class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user =  UserModel.objects.get(id=uid)

        except(TypeError,ValueError,OverflowError,UserModel.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user,token):
            user.is_active=True
            user.save()
            messages.success(request,"Hesabınız başarıyla aktifleştirilmiştir.")
            return redirect("url_login")
        else:
            messages.error(request,"Geçersiz onay linki!")
            return redirect("url_register")


class UserLoginView(View):
    http_method_names = ["get","post"]


    def get(self,request):
        return render(request,"account/signin.html")

    def post(self,request):

        email = self.request.POST.get("email")
        password = self.request.POST.get("password")
        user = authenticate(email=email, password=password)
        if user is None:
            messages.error(request, "Giriş bilgileri hatalı.")
            return redirect("url_login")
        else:
            try:
                cart = CartModel.objects.get(cart_id = _cart_id(request))
                is_cart_item_exists = CartItemModel.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_items      = CartItemModel.objects.filter(cart=cart)
                    for item in cart_items:
                        item.user = user
                        item.save()
            except:
                pass
            login(request, user)
            messages.success(request, "Giriş işlemi başarılı.")
            return redirect("url_homePage")


class LogoutView(LoginRequiredMixin,View):
    http_method_names = ["get"]
    def get(self,request):
        logout(request)
        messages.success(request,"Başarıyla Çıkış Yapıldı")
        return redirect("url_homePage")


class ProfileView(LoginRequiredMixin,View):
    http_method_names = ["get"]

    def get(self,request):
        orders = OrderModel.objects.filter(user=request.user).order_by("-created_date")
        order_count = orders.count()
        ctx={
            "orders":orders,
            "order_count":order_count
        }
        return render(request,"account/dashboard.html",ctx)


class MyOrdersView(LoginRequiredMixin,ListView):
    template_name       = "account/my-orders.html"
    context_object_name = "orders"
    paginate_by         = 5
    def get_queryset(self):
        return OrderModel.objects.filter(user=self.request.user).order_by("-created_date")


class OrderDetailView(DetailView):
    template_name       = "orders/order-detail.html"
    context_object_name = "order"

    def get_object(self, queryset=None):
        return OrderModel.objects.get(order_number=self.kwargs.get("order_number"))


class ForgotPassword(View):
    http_method_names = ["get","post"]
    def get(self,request):
        return render(request,"account/forgot-password.html")

    def post(self,request):
        email = request.POST.get("email")
        user = UserModel.objects.filter(email=email)
        if user.exists():
            user=user[0]
            try:
                with transaction.atomic():
                    current_site = get_current_site(self.request)
                    mail_subject = "Şifre Sıfırlama"
                    message = render_to_string("account/reset_password_mail.html", {
                        "user": user,
                        "domain": current_site,
                        "uid": urlsafe_base64_encode(force_bytes(user.id)),
                        "token": default_token_generator.make_token(user)
                    })
                    to_email = user.email
                    send_email = EmailMessage(mail_subject, message, to=[to_email], )
                    send_email.send()
                    messages.success(self.request, "Şifre sıfırlama maili başarıyla gönderildi.")
            except Exception as e:
                messages.error(self.request, "Bir Sorun Oluştu. Lütfen sonra tekrar deneyiniz.")
        else:
            messages.error(request,"Bu mail adresine kayıtlı bir hesap bulunamadı.")
        return redirect("url_forgotPassword")


class ResetPasswordValidateView(View):
    http_method_names = ["get","post"]
    def get(self,request,uidb64,token):
        uid = urlsafe_base64_decode(uidb64).decode()
        try:
            user = UserModel.objects.get(id=uid)

        except(TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            request.session["uid"] = uid
            messages.success(request,"Lütfen şifrenizi sıfırlayınız.")
            return redirect("url_resetPassword")
        else:
            messages.error(request,"Bu aktivasyon linki geçersizdir.")
            return redirect("url_login")


class ResetPasswordView(View):
    http_method_names = ["get","post"]

    def get(self,request):

        return render(request, "account/reset_password.html")

    def post(self,request):
        password         = request.POST.get("password")
        password_confirm = request.POST.get("password_confirm")
        if password_confirm == password:
            uid = request.session.get("uid")
            user = UserModel.objects.get(id=uid)
            user.set_password(password)
            user.save()
            messages.success(request,"Şifreniz başarıyla güncellendi.")
            return redirect("url_login")
        else:
            messages.error(request,"Parolalar eşleşmiyor.")
            return redirect("url_resetPassword")


class ChangePasswordView(LoginRequiredMixin,View):
    def get(self,request):
        form = PasswordChangeForm(request.user)
        ctx={"form":form}
        return render(request,"account/change-password.html",ctx)

    def post(self,request):
        form = PasswordChangeForm(request.user, request.POST)
        ctx={"form":form}
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request,"Parola başarıyla güncellendi")
        return render(request,"account/change-password.html",ctx)