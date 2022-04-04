from django.db import models
from django.db.models import Avg
from unidecode import unidecode
from autoslug import AutoSlugField
from django.template.defaultfilters import slugify
from category.models import CategoryModel
from django.shortcuts import reverse
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class ProductModel(models.Model):
    product_name = models.CharField(max_length=100,verbose_name=_("Product Name")
,help_text=_("Product Name")
)
    slug         = AutoSlugField(populate_from="product_name",
                         null=True, unique=True, editable=False,
                         verbose_name="Slug",help_text="Slug")
    description   = models.TextField(max_length=500,verbose_name=_("Product Detail"))
    price         = models.PositiveIntegerField(verbose_name=_("Product Price"))
    images        = models.ImageField(upload_to="photos/products",verbose_name=_("Image"))
    stock         = models.PositiveIntegerField(verbose_name=_("Stock"))
    is_available  = models.BooleanField(default=True,verbose_name=_("Active"))
    category      = models.ForeignKey(CategoryModel,verbose_name=_("Categories"),on_delete=models.CASCADE)
    created_date  = models.DateTimeField(auto_now_add=True,verbose_name=_("Created Date"))
    modified_date = models.DateTimeField(auto_now=True,verbose_name=_("Modified Date"))

    def average_review(self):
        reviews = ReviewRatingModel.objects.filter(product=self,status=True).aggregate(average=Avg("rating"))
        avg = 0
        if reviews["average"] is not None:
            avg =float(reviews["average"])
        return avg

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.id is None:
            self.slug = slugify(unidecode(self.product_name))
        super(ProductModel, self).save()

    def get_url(self):
        return reverse("url_productDetail",args=[self.category.slug,self.slug])

    def __str__(self):
        return f"{self.product_name}"


    class Meta:
        verbose_name        = _("Product")
        verbose_name_plural = _("Products")
        db_table            = "Products"
        ordering = ['id']


VARIATION_CATEGORY_CHOICES=(
    ("color","Renk"),
    ("size","Beden")
)

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category="color",is_active=True)
    def sizes(self):
        return super(VariationManager, self).filter(variation_category="size",is_active=True)


class ProductVariationModel(models.Model):
    product            = models.ForeignKey(ProductModel,on_delete=models.CASCADE,related_name="variations",verbose_name=_("Product"))
    variation_category = models.CharField(max_length=150,choices=VARIATION_CATEGORY_CHOICES,verbose_name=_("Variation Category"))
    variation_value    = models.CharField(max_length=100,verbose_name=_("Variation Value"))
    is_active          = models.BooleanField(default=True,verbose_name=_("Is Active"))
    created_date       = models.DateTimeField(auto_now_add=True,verbose_name=_("Created Date"))
    objects            = VariationManager()

    def __str__(self):
        return self.variation_value


    class Meta:
        verbose_name        = _("Product Variation")
        verbose_name_plural = _("Product Variations")
        db_table            = "ProductVariations"
        ordering = ['-id']


class ReviewRatingModel(models.Model):
    product = models.ForeignKey(ProductModel,on_delete=models.CASCADE,verbose_name=_("Product"),related_name="reviews")
    user    = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name=_("User"))
    subject = models.CharField(max_length=50,blank=True,verbose_name=_("Subject"))
    review  = models.TextField(max_length=250, blank=True,verbose_name=_("Review"))
    rating  = models.FloatField(verbose_name=_("Rating"))
    ip      = models.CharField(max_length=50,blank=True,verbose_name=_("IP Address"))
    status  = models.BooleanField(default=True,verbose_name=_("Status"))
    created_date = models.DateTimeField(auto_now_add=True,verbose_name=_("Created Date"))
    update_date = models.DateTimeField(auto_now=True,verbose_name=_("Update Date"))

    class Meta:
        verbose_name        = _("Product Review")
        verbose_name_plural = _("Product Teviews")
        db_table            = "ProductReviews"

    def __str__(self):
        return self.subject


class ProductGalleryModel(models.Model):
    product = models.ForeignKey(ProductModel,on_delete=models.CASCADE,verbose_name=_("Product"),default=None,related_name="product_images")
    image   = models.ImageField(upload_to="store/products",max_length=300,verbose_name=_("Image"))

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name        = _("Product Images")
        verbose_name_plural = _("Product Images")
        db_table            = "ProductImages"