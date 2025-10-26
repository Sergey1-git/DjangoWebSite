from django.http import HttpResponse
from django.shortcuts import render

from .forms import AddProductForm

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

def contact(request):
    return HttpResponse("Обратная связь")
