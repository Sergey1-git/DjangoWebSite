from django.shortcuts import render
from .forms import FormBasket

from django import forms

from flower.models import Flower

dict_object_basket = {}
dict_object_basket_form={}

class Basket:
    def __init__(self, id):
        self.id_object=id
        self.args={}


    def add_flower_basket(id, *args):
        if len(args)==2:
            if args[0] not in dict_object_basket[id].args:
                dict_object_basket[id].args[args[0]]=args[1]
            else:
                dict_object_basket[id].args[args[0]]+=1


    def delete_basket_and_form(id):
        del dict_object_basket[id]
        del dict_object_basket_form[id]



def object_basket(id_user, *args):
    print('вход object_basket', id_user, *args)
    flag = True
    if len(dict_object_basket)>0:
        for  key in dict_object_basket:
           if dict_object_basket[key].id_object==id_user:
               flag = False
    if flag:
        dict_object_basket[id_user]=Basket(id_user)
        Basket.add_flower_basket(id_user, *args)
    else:
        Basket.add_flower_basket(id_user, *args)


def basket(request):

    if request.method == "GET" and len(dict_object_basket) > 0:
        user_id = request.user.id
        dict_data=dict_object_basket[user_id].args
        dict_object_basket_form[user_id]=FormBasket(preparation_form(dict_data, user_id))

        return render(request, 'basket/basket.html',{'title': 'Корзина покупок',
                             'form': dict_object_basket_form[user_id],'args': len(dict_object_basket[user_id].args),})


    if len(dict_object_basket)==0:
        return render(request, 'basket/basket.html',{'title': 'Ваша корзина покупок пуста','args':0,})


def preparation_form(dict_data, user_id):
    dict_all = {}
    dict_cost = {}
    for key in dict_data:
        initial = dict_object_basket[user_id].args[key]
        w1 = Flower.objects.get(pk=key)
        string = str(w1.id)
        dict_all[string] = forms.IntegerField(min_value=0,
                                              max_value=w1.quantity + initial, initial=initial, label=w1.title)
        dict_cost[w1.id] = w1.price * dict_object_basket[user_id].args[key]
    cost_order = 0
    for key in dict_cost:
        cost_order += dict_cost[key]
    dict_all['cost'] = forms.IntegerField(label='Общая стоимость заказа', initial=cost_order,
                                          widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    dict_all['address'] = forms.CharField(max_length=255, label='Адрес доставки')
    dict_all['id_user'] = forms.CharField(widget=forms.HiddenInput(), initial=user_id)
    return dict_all
