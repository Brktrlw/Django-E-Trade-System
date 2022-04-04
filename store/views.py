from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, ListView , FormView
from orders.models import OrderProductModel
from store.models import ProductModel,CategoryModel
from .forms import ReviewForms


class ListProductView(ListView):
    template_name = "store/store.html"
    context_object_name = "products"
    paginate_by = 3
    model = ProductModel

    def get_queryset(self):
        products = self.get_products()
        if self.request.GET.get("ordering"):
            products = self.order_product(self.request.GET.get("ordering"))
        return products

    def get_products(self):
        if self.kwargs.get("category_slug"):
            get_object_or_404(CategoryModel,slug=self.kwargs.get("category_slug"))
            products = ProductModel.objects.filter(is_available=True, category__slug=self.kwargs.get("category_slug"))
        else:
            products = ProductModel.objects.filter(is_available=True)
        return products

    def order_product(self,orderType):
        products = self.get_products()
        if orderType == "price" or "-price":
            try:
                products = products.order_by(orderType)
            except:
                pass
        return products


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ListProductView, self).get_context_data(**kwargs)
        productCount=self.get_queryset().count()
        context["productCount"]  = productCount
        context["category_name"] = self.kwargs.get("category_slug")
        return context


class ProductDetailView(DetailView):
    template_name       = "store/product-detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        product = kwargs.get("object")
        reviews = product.reviews.all()
        ctx = super(ProductDetailView, self).get_context_data(**kwargs)
        print(product.product_images.all())
        ctx["reviews"] = reviews

        try:
            ctx["isOrder"] = OrderProductModel.objects.filter(user=self.request.user,product=product).exists()
        except:
            ctx["isOrder"] = False
        return ctx


    def get_object(self, queryset=None):
        return get_object_or_404(ProductModel,slug=self.kwargs.get('product_slug'),category__slug=self.kwargs.get("category_slug"))


class SearchListView(ListView):
    template_name       = "store/store.html"
    model               = ProductModel
    context_object_name = "products"

    #def get_context_object_name(self, object_list):
    #    super(SearchListView, self).get_context_object_name(object_list)

    def get_queryset(self):
        search_query = self.request.GET.get("keyword",None)

        if search_query:
            return ProductModel.objects.filter(Q(product_name__icontains=search_query) | Q(description__icontains=search_query))


    def get_context_data(self, *, object_list=None, **kwargs):
        context                 = super(SearchListView, self).get_context_data(**kwargs)
        productCount            = self.get_queryset().count()
        context["productCount"] = productCount
        return context



class ReviewFormView(FormView):
    form_class    = ReviewForms

    def get_product(self):
        return get_object_or_404(ProductModel,id=self.request.POST.get("product"))

    def form_valid(self, form):
        product = self.get_product()
        reviewObj  = form.save(commit=False)
        reviewObj.user =self.request.user
        reviewObj.product = product
        reviewObj.ip = self.request.META.get("REMOTE_ADDR")
        form.save()
        messages.success(self.request,"Yorum yapma işlemi başarılı.")
        return redirect("url_productDetail",product.category.slug,product.slug)

    def form_invalid(self, form):
        messages.error(self.request,"Lütfen yorum için eksik alanları doldurunuz")
        return redirect("url_productDetail", self.get_product().category.slug, self.get_product().slug)

