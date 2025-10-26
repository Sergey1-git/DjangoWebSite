from django import forms
from flower_shop.flower.models import Flower


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Flower
        fields = ['title', 'content', 'plant_type','price', 'quantity', 'photo']