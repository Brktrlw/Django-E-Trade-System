from django.shortcuts import render
from django.views.generic import View,ListView

from store.models import ProductModel

class HomePageView(View):
    http_method_names = ["get"]

    def get(self,request):
        ctx = dict()
        products = ProductModel.objects.filter(is_available=True)
        ctx["products"]=products
        return render(request,"home.html",ctx)

