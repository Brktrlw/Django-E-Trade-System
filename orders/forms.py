from django import forms
from .models import OrderModel



class OrderForm(forms.ModelForm):
    class Meta:
        model  = OrderModel
        fields = ("first_name","last_name","email","phone","address_title","city","clear_address","order_note")