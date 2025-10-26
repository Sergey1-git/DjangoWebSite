from django.shortcuts import render

menu = [{'title': "Главная страница", 'url_name': 'home'},
        {'title': "Контакты", 'url_name': 'contact'},
]


def index(request):
    date={'title': 'Главная страница','menu': menu,'posts': 'db.sqlite3',}
    return render(request, 'flower/index.html', context=date)

