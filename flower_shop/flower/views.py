from django.http import HttpResponse
from django.shortcuts import render

from .forms import AddProductForm
from .models import Flower

menu = [{'title': "Главная страница", 'url_name': 'home'},
        {'title': "Добавить товар", 'url_name': 'add_product'},
        {'title': "Контакты", 'url_name': 'contact'},
]


def index(request):
    date={'title': 'Главная страница','menu': menu,'posts': 'db.sqlite3',}
    return render(request, 'flower/index.html', context=date)


def add_product(request):

    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            print('Valid add_product')
            form.save()
        else:
            print('NO Valid add_product')
            return render(request, 'flower/product.html', {'title': 'Добавление товара', 'menu': menu, 'form': form, })
    form = AddProductForm()
    return render(request, 'flower/product.html',{'title': 'Добавление товара','menu': menu,'form': form,})


def homemade_flowers(request):

    data_dbh = Flower.objects.filter(plant_type='home')
    if request.method == "POST":
        dict=request.POST.dict()
        if 'buy' in dict:
            id=request.user.id
            buy_flower(request,id, dict['id'], dict['buy'])
        return render(request, 'flower/homemade_flowers.html',{'title': 'Домашние цветы','menu': menu,'posts': data_dbh,})
    return render(request, 'flower/homemade_flowers.html',{'title': 'Домашние цветы','menu': menu,'posts': data_dbh,})

def contact(request):
    return HttpResponse("Обратная связь")


def buy_flower(request, id_user, id_flower, name_flower):
    pass
