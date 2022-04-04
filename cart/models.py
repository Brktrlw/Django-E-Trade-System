import uuid
from django.conf import settings
from django.db import models
from store.models import ProductModel
from store.models import ProductVariationModel
from django.utils.translation import ugettext_lazy as _

class CartModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE,verbose_name=_("User"),
                                   help_text=_("User"),null=True)
    cart_id    = models.CharField(unique=True,
                                  verbose_name=_("Cart ID"),
                                  help_text=_("Cart ID"),blank=True,max_length=250)
    date_added = models.DateField(auto_now_add=True,verbose_name=_("Created Date"),help_text=_("Created Date"))

    def __str__(self):
        return str(self.cart_id)

    class Meta:
        verbose_name        = _("Cart")
        verbose_name_plural = _("Carts")
        db_table            = "Carts"


class CartItemModel(models.Model):
    user       = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE,verbose_name=_("User"),
                                   help_text=_("User"),null=True)
    product    = models.ForeignKey(ProductModel,on_delete=models.CASCADE,
                                   verbose_name=_("Product"),help_text=_("Product"))
    cart       = models.ForeignKey(CartModel,on_delete=models.CASCADE,
                                   verbose_name=_("Cart"),help_text=_("Cart"),
                                   related_name="products",null=True)
    quantity   = models.PositiveIntegerField(verbose_name=_("Quantity"),help_text=_("Quantity"))
    is_active  = models.BooleanField(default=True,verbose_name=_("Active"),help_text=_("Active"))
    variations = models.ManyToManyField(ProductVariationModel,blank=True)
    unique_id  = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        verbose_name        = _("Cart Item")
        verbose_name_plural = _("Cart Items")
        db_table            = "CartItems"

    def __str__(self):
        return f"{self.product}"

    def get_sub_total(self):
        return self.product.price * self.quantity

