from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/",include("admin_honeypot.urls",namespace="admin_honeypot")),
    path('securelogin/', admin.site.urls),
    path("store/",include("store.urls")),
    path("cart/",include("cart.urls")),
    path("",include("pages.urls")),
    path("user/",include("accounts.urls")),
    path("orders/",include("orders.urls")),
    path('rosetta/', include('rosetta.urls')),

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)