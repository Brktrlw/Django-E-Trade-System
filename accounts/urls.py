
from django.urls import path
from .views import (UserLoginView, RegisterView,
                    LogoutView, ActivateAccountView,
                    ProfileView, ForgotPassword, ResetPasswordValidateView,
                    ResetPasswordView, MyOrdersView, EditProfileView,
                    ChangePasswordView, OrderDetailView)

urlpatterns = [
    # Basic User
    path("register/",RegisterView.as_view(),name="url_register"),
    path("login/",UserLoginView.as_view(),name="url_login"),
    path("logout/",LogoutView.as_view(),name="url_logout"),
    path("profile/",ProfileView.as_view(),name="url_profile"),
    path("edit-profile/",EditProfileView.as_view(),name="url_editProfile"),
    # Password
    path("forgot-password/",ForgotPassword.as_view(),name="url_forgotPassword"),
    path("reset-passwd/<uidb64>/<token>/",ResetPasswordValidateView.as_view(),name="url_resetPasswordValidate"),
    path("reset-password/",ResetPasswordView.as_view(),name="url_resetPassword"),
    path("change-password/", ChangePasswordView.as_view(), name="url_changePassword"),
    #Active User Account with mail
    path("activate/<uidb64>/<token>/",ActivateAccountView.as_view(),name="url_activate"),

    # orders
    path("my-orders/",MyOrdersView.as_view(),name="url_myOrders"),
    path("order-detail/<str:order_number>",OrderDetailView.as_view(),name="url_orderDetail")



]