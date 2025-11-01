from django.shortcuts import render
from  basket.forms import FormBasket
from django import forms
from  flower.models import Flower
from basket.models import BasketModel

dict_object_basket = {}
dict_object_basket_form={}


# Класс корзины покупателей.
class Basket:
    def __init__(self, id):
        self.id_object=id
        self.args={}

    # Функция добавления в Корзинe покупателя товара.
    def add_flower_basket(id, *args):
        if len(args)==2:
            if args[0] not in dict_object_basket[id].args:
                dict_object_basket[id].args[args[0]]=args[1]
            else:
                dict_object_basket[id].args[args[0]]+=1

    # Удаление корзины покупателя и формы заказа.
    def delete_basket_and_form(id):
        del dict_object_basket[id]
        del dict_object_basket_form[id]


# Функция создания Корзины покупателя при первом нажатии кнопки купить.
def object_basket(id_user, *args):
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

# Основная функция корзины.
def basket(request):
    # Формирование представления предварительной формы заказа в Корзине.
    if request.method == "GET":
        user_id = request.user.id
        if user_id in dict_object_basket:
            dict_data = dict_object_basket[user_id].args
            dict_object_basket_form[user_id] = FormBasket(preparation_form(dict_data, user_id))
            return render(request, 'basket/basket.html', {'title': 'Корзина покупок',
                             'form': dict_object_basket_form[user_id],'args': len(dict_object_basket[user_id].args),})
        else:
            return render(request, 'basket/basket.html', {'title': 'Корзина покупок', 'args': 0,})

    # Формирование заказа в Корзине.
    if request.method == "POST":
        user_id = request.user.id
        dict_data = request.POST.dict()
        dict_order = {}
        dict_order_0 = {}
        for key in dict_data:
            if key not in ['id_user', 'cost', 'address', 'csrfmiddlewaretoken', 'recalculation', 'product']:
                dict_order_0[key] = int(dict_data[key])
                if dict_data[key]!='0':
                    dict_order[key] = int(dict_data[key])
        # Проверка изменений внесенных  покупателем в Корзине относительно первоначального содержания.
        if 'recalculation' in dict_data:
            correct_db(user_id, dict_order_0)
            if len(dict_order) != 0:
                dict_object_basket[user_id].args = dict_order
                dict_object_basket_form[user_id] = FormBasket(preparation_form(dict_order, user_id))
                return render(request, 'basket/basket.html',{'title': 'Корзина покупок',
                            'form': dict_object_basket_form[user_id],'args': len(dict_object_basket[user_id].args), })
            else:
                Basket.delete_basket_and_form(user_id)
                return render(request, 'basket/basket.html',{'title': 'Корзина покупок','args': 0,})

        # Если изменения в Корзине не было запись заказа в базу данных.
        else:
            dict_object_basket_form[user_id].data=request.POST
            dict_object_basket_form[user_id].is_bound = True
            if  dict_object_basket_form[user_id].is_valid():
                print('Valid')
                data = dict_object_basket_form[user_id].data
                dict_order_final = {}
                for key in data:
                    if key not in ['id_user', 'cost', 'address', 'csrfmiddlewaretoken', 'recalculation', 'product']:
                        dict_order_final[key] = int(data[key])
                w2 = BasketModel(id_users=int(data.get('id_user')), dict_order=dict_order, cost=float(data.get('cost')),
                             address=data.get('address'))
                w2.save()
                Basket.delete_basket_and_form(user_id)
                string = 'Заказ успешно создан'
                return render(request, 'basket/basket.html', {'title': 'Заказ успешно создан', 'string':string, })
            else:
                print('NO Valid')
                form = dict_object_basket_form[user_id]
                string = 'Что то пошло не так, попробуйте повторить заказ '
                return render(request, 'basket/basket.html',{'title': 'Что то пошло не так, попробуйте'
                                                                  ' повторить заказ ','string':string,'form': form,})


# Функция подготовки формы заказа изменяемой динамически.
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


 # Корректировка колличества товара на складе после изменений в заказе.
def correct_db(user_id, dict_order_recalc):
    for key in dict_order_recalc:
        w3 = Flower.objects.get(pk=int(key))
        value_before = dict_object_basket[user_id].args[key]
        if dict_order_recalc[key] == value_before:
            w3.quantity = w3.quantity
        elif dict_order_recalc[key] > value_before:
            w3.quantity -= dict_order_recalc[key] - value_before
            w3.save()
        else:
            w3.quantity += value_before - dict_order_recalc[key]
            w3.save()