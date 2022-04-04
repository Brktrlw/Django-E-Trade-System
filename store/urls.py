from django.urls import path
from .views import ProductDetailView,ListProductView,SearchListView,ReviewFormView


urlpatterns = [
    path("",ListProductView.as_view(),name="url_store"),
    path("category/<slug:category_slug>/",ListProductView.as_view(),name="url_productsByCategory"),
    path("category/<slug:category_slug>/<slug:product_slug>/",ProductDetailView.as_view(),name="url_productDetail"),
    path("search/",SearchListView.as_view(),name="url_searchProduct"),

    path("create-review/",ReviewFormView.as_view(),name="url_createReview"),

]