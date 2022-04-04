from django import forms
from .models import ReviewRatingModel

class ReviewForms(forms.ModelForm):
    subject = forms.CharField(max_length=100,required=True)
    review  = forms.CharField(max_length=250,required=True)
    rating  = forms.FloatField(required=True)
    class Meta:
        model  = ReviewRatingModel
        fields = ["subject","review","rating","product"]