from django.contrib import admin
from django.utils.html import format_html
from .models import UserModel, UserProfileModel
from django.contrib.auth.admin import UserAdmin
from parler.admin import TranslatableAdmin


class ProfileInline(admin.TabularInline):
    model = UserProfileModel
    extra = 0

class CustomUserAdmin(admin.ModelAdmin):
    model        = UserModel
    list_display = ("username","email")
    fieldsets    =  UserAdmin.fieldsets +(
        ("Extra",{
            "fields":["phone_number"]
        }),
    )
    inlines = [ProfileInline]

admin.site.register(UserModel,CustomUserAdmin)



@admin.register(UserProfileModel)
class UserProfile(TranslatableAdmin):

    def thumbnail(self,object):
        return format_html(f"<img src='{object.avatar.url}' width='30' style='border-radius:50%'>")


    thumbnail.short_description = "Profil Fotoğrafı"
    list_display                = ["thumbnail","user","address_title","city"]


