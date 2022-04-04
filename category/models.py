from django.db import models
from unidecode import unidecode
from autoslug import AutoSlugField
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

class CategoryModel(models.Model):
    category_name = models.CharField(max_length=100,unique=True,verbose_name=_("Category Name"),help_text=_("Category Name"))
    slug          = AutoSlugField(populate_from="category_name",null=True,unique=True,editable=False,verbose_name="Slug",help_text="Slug")
    description   = models.TextField(max_length=500,help_text=_("Detail"),verbose_name=_("Detail"))
    image         = models.ImageField(upload_to="photos/categories/",blank=True,null=True)

    def __str__(self):
        return f"{self.category_name}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.id is None:
            self.slug = slugify(unidecode(self.category_name))
        super(CategoryModel, self).save()

    class Meta:
        verbose_name        = _("Category")
        verbose_name_plural = _("Categories")
        db_table            = "Categories"


