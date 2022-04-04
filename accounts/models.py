from django.db import models
from django.contrib.auth.models import AbstractBaseUser,AbstractUser
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

class UserModel(AbstractUser):
    phone_number = models.CharField(max_length=15,help_text=_("Phone Number"),verbose_name=_("Phone Number"))
    email        = models.EmailField(unique=True,max_length=200,verbose_name=_("Email"))
    REQUIRED_FIELDS = ["first_name","last_name","username"]
    USERNAME_FIELD = "email"

    class Meta:
        verbose_name        = _("User")
        verbose_name_plural = _("Users")
        db_table            = "Users"

    def __str__(self):
        return self.username


class UserProfileModel(models.Model):
    user          = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name=_("User"))
    address_title = models.CharField(max_length=100,verbose_name=_("Address Title"))
    city          = models.CharField(max_length=100,verbose_name=_("City"))
    clear_address = models.TextField(max_length=250,verbose_name=_("Clear Address"))
    avatar        = models.ImageField(blank=True,upload_to="userprofile/",default="default/user.jpg",verbose_name=_("Photo"))

    def __str__(self):
        return str(self.user)

    class Meta:
        db_table            = "Profiles"
        verbose_name        = _("Profile")
        verbose_name_plural = _("Profiles")
