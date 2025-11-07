from django import forms

from .models import Flower, ContactModel


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Flower
        fields = ['title', 'content', 'plant_type','price', 'quantity', 'photo']


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactModel
        fields = ['first_name', 'last_name', 'email','content']
        labels = {
            'first_name': ("Имя"),'last_name': ("Фамилия"),'email': ("Электронная почта"),'content': ("Текст сообщения"),
        }