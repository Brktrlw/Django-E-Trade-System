from django.contrib import admin

from .models import CategoryModel


@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display        = ["category_name","slug","description"]
    list_display_links  = ["category_name"]
    search_fields       = ["category_name"]
    list_filter         = ["slug"]
    readonly_fields     = ["slug"]

    class Meta:
        model=CategoryModel
