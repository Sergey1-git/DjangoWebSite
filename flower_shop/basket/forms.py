from django import forms

class FormBasket(forms.Form):


    def __init__(self, dict_all, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавление полей из словаря
        for name, field_class in dict_all.items():
            if name !='csrfmiddlewaretoken':
                self.fields[name] = field_class
        self.post=None