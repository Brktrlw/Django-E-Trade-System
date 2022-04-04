from django.contrib import admin
from .models import ProductModel, ProductVariationModel, ReviewRatingModel, ProductGalleryModel
import admin_thumbnails

class RatingInline(admin.TabularInline):
    model = ReviewRatingModel
    extra = 0

@admin_thumbnails.thumbnail("image")
class ProductImagesInline(admin.TabularInline):
    model = ProductGalleryModel
    extra = 0

@admin.register(ReviewRatingModel)
class ReviewRatingAdmin(admin.ModelAdmin):
    list_display        = ["product","user","subject","rating","status"]
    list_display_links  = ["product",]
    search_fields       = ["product"]
    list_filter         = ["created_date"]


    class Meta:
        model=ProductModel

@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):

    def review_avarege(self,obj):
        return obj.average_review()

    list_display        = ["product_name","slug","price","stock","review_avarege"]
    list_display_links  = ["slug",]
    search_fields       = ["product_name"]
    list_filter         = ["created_date"]
    list_editable       = ("price","stock","product_name")
    readonly_fields     = ("slug",)
    inlines             = [RatingInline,ProductImagesInline]

    class Meta:
        model=ProductModel


@admin.register(ProductVariationModel)
class ProductVariationAdmin(admin.ModelAdmin):
    list_display        = ["product","variation_category","variation_value"]
    list_display_links  = ["product",]

    class Meta:
        model = ProductVariationModel

admin.site.register(ProductGalleryModel)