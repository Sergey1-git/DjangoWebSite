from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .forms import AddProductForm
from .models import Flower
from basket.views import object_basket


menu = [{'title': "Главная страница", 'url_name': 'home'},
        {'title': "Добавить товар", 'url_name': 'add_product'},
        {'title': "Контакты", 'url_name': 'contact'},]


# Функция  представления главной страницы.
def index(request):
    date = {'title': 'Главная страница','menu': menu,'posts': 'db.sqlite3',}
    return render(request, 'flower/index.html', context=date)


# Функция  добавления в базу данных товара.
def add_product(request):
    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        else:
            return render(request, 'flower/product.html', {'title': 'Добавление товара', 'menu': menu, 'form': form, })
    form = AddProductForm()
    return render(request, 'flower/product.html',{'title': 'Добавление товара','menu': menu,'form': form,})


# Функция  представления каталого комнатные цветы.
def homemade_flowers(request):
    data_dbh = Flower.objects.filter(plant_type='home')
    if request.method == "POST":
        dict=request.POST.dict()
        if 'buy' in dict:
            if request.user.is_authenticated is False:
                return HttpResponseRedirect("/users/register/")
            else:
                id = request.user.id
                buy_flower(request, id, dict['id'], dict['buy'])
    return render(request, 'flower/homemade_flowers.html',
                      {'title': 'Домашние цветы', 'menu': menu, 'posts': data_dbh, })

# Функция  представления каталого садовые цветы.
def garden_flowers(request):
    data_dbh = Flower.objects.filter(plant_type='garden')
    if request.method == "POST":
        dict=request.POST.dict()
        if 'buy' in dict:
            if request.user.is_authenticated is False:
                return HttpResponseRedirect("/users/register/")
            else:
                id = request.user.id
                buy_flower(request, id, dict['id'], dict['buy'])
    return render(request, 'flower/garden_flowers.html',
                      {'title': 'Садовые цветы', 'menu': menu, 'posts': data_dbh, })


# Функция  представления товара на его персональной странице.
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

# Функция  представления контактов магазина.
def contact(request):
    date = {'title': 'Обратная связь', 'menu': menu, }
    return render(request, 'flower/contact.html', context=date)


# Функция  изменения колличеста товара в базе данных при нажатии кнопки купить,
# а также отправки сведений в Корзину покупателя.
def buy_flower(request, id_user, id_flower, name_flower):
    w = Flower.objects.get(pk=id_flower)
    if w.quantity > 0:
        w.quantity -= 1
        object_basket(id_user, id_flower, 1)
        w.time_create = datetime.now()
        w.is_published = True
        w.save()
