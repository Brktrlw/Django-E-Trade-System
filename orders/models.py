from django.db import models
from django.conf import settings
from store.models import ProductModel, ProductVariationModel
from django.utils.translation import ugettext_lazy as _

STATUS = (
    ("New",_("New Order")),
    ("Receipt", _("Receipt")),
    ("Completed", _("Completed")),
    ("Canceled", _("Canceled")),
)
class OrderModel(models.Model):
    user           = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,
                                       verbose_name=_("User"))
    order_number   = models.CharField(max_length=100,verbose_name=_("Order Number"))
    first_name     = models.CharField(max_length=50,verbose_name=_("First Name"))
    last_name      = models.CharField(max_length=50,verbose_name=_("Last Name"))
    phone          = models.CharField(max_length=50,verbose_name=_("Phone"))
    email          = models.EmailField(max_length=50,verbose_name=_("Email"))
    address_title  = models.CharField(max_length=50,verbose_name=_("Address Title"))
    city           = models.CharField(max_length=50,verbose_name=_("City"))
    clear_address  = models.CharField(max_length=500,verbose_name=_("Clear Address"))
    order_note     = models.CharField(max_length=400,verbose_name=_("Order Note"))
    order_total    = models.FloatField(verbose_name=_("Order Total"))
    tax            = models.FloatField(verbose_name=_("Tax"))
    status         = models.CharField(max_length=20,choices=STATUS,default="New",verbose_name=_("Status"))
    ip             = models.CharField(max_length=20,blank=True,verbose_name=_("IP Address"))
    is_ordered     = models.BooleanField(default=False,verbose_name=_("Is Ordered"))
    created_date   = models.DateTimeField(auto_now_add=True,verbose_name=_("Created Date"))
    update_date    = models.DateTimeField(auto_now=True,verbose_name=_("Update Date"))

    def get_fullname(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_address(self):
        return f"{self.address_title} {self.city} {self.clear_address}"

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name        = _("Order")
        verbose_name_plural = _("Orders")
        db_table            = "Orders"


class OrderProductModel(models.Model):
    order         = models.ForeignKey(OrderModel,on_delete=models.CASCADE,related_name="products",verbose_name=_("Order"))
    user          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name=_("User"))
    product       = models.ForeignKey(ProductModel,on_delete=models.CASCADE,verbose_name=_("Product"))
    variation     = models.ManyToManyField(ProductVariationModel,blank=True,verbose_name=_("Product Variation"))
    quantity      = models.PositiveIntegerField(verbose_name=_("Quantity"))
    product_price = models.FloatField(verbose_name=_("Product Price"))
    ordered       = models.BooleanField(default=False,verbose_name=_("Ordered"))
    status        = models.CharField(max_length=100,verbose_name=_("Status"))
    created_add   = models.DateTimeField(auto_now_add=True,verbose_name=_("Created Add"))

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name        = _("Order Product")
        verbose_name_plural = _("Order Products")
        db_table            = "OrderProducts"
