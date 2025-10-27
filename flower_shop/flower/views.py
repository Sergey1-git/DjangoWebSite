from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .forms import AddProductForm
from .models import Flower
from basket.views import object_basket


menu = [{'title': "Главная страница", 'url_name': 'home'},
        {'title': "Добавить товар", 'url_name': 'add_product'},
        {'title': "Контакты", 'url_name': 'contact'},
]


def index(request):
    date = {'title': 'Главная страница','menu': menu,'posts': 'db.sqlite3',}
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


def garden_flowers(request):

    data_dbh = Flower.objects.filter(plant_type='garden')
    if request.method == "POST":
        dict=request.POST.dict()
        if 'buy' in dict:
            id=request.user.id
            buy_flower(request,id, dict['id'], dict['buy'])
        return render(request, 'flower/garden_flowers.html',{'title': 'Садовые цветы','menu': menu,'posts': data_dbh,})
    return render(request, 'flower/garden_flowers.html',{'title': 'Садовые цветы','menu': menu,'posts': data_dbh,})



def show_post(request, id):

    if request.method == "POST":
        dict = request.POST.dict()
        if 'buy' in dict:
            id_user = request.user.id
            buy_flower(request, id_user, dict['id'], dict['buy'])
    post = get_object_or_404(Flower, pk=id)

    data = {
        'title': post.title,
        'menu': menu,
        'post': post,}

    return render(request, 'flower/post.html', context=data)


def contact(request):
    return HttpResponse("Обратная связь")


def buy_flower(request, id_user, id_flower, name_flower):
    print("buy_flower request.POST.dict()", request.POST.dict())
    print('Вход buy_flower', id_user, id_flower, name_flower)
    w = Flower.objects.get(pk=id_flower)
    if w.quantity > 0:
        w.quantity -= 1
        print('id_user buy_flower',id_user)
        object_basket(id_user, id_flower, 1)
        w.time_create = datetime.now()
        w.is_published = True
        w.save()
