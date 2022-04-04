from .models import UserModel, UserProfileModel
from django.contrib.auth.forms import UserCreationForm
from django import forms


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50,required=True)
    last_name  = forms.CharField(max_length=50,required=True)
    email      = forms.EmailField(max_length=100,required=True)
    password1  = forms.CharField(max_length=200,required=True,widget=forms.PasswordInput())
    password2  = forms.CharField(max_length=200,required=True,widget=forms.PasswordInput())

    class Meta:
        model = UserModel
        fields= ["first_name","last_name","email","username","password1","password2"]

    def clean(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password2 == password1:
            return self.cleaned_data
        raise forms.ValidationError("Parolalar Eşleşmiyor")


class LoginForm(forms.ModelForm):
    class Meta:
        model  = UserModel
        fields = ["email","password"]


class UserProfileForm(forms.ModelForm):
    first_name    = forms.CharField(max_length=100,required=True)
    last_name     = forms.CharField(max_length=100,required=True)
    phone_number  = forms.CharField(max_length=100,required=True)
    city          = forms.CharField(max_length=100,required=True)
    address_title = forms.CharField(max_length=100,required=True)

    class Meta:
        model  = UserProfileModel
        fields = ["city","clear_address","avatar","address_title"]








