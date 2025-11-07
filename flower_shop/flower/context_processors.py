from .views import menu


def get_flower_context(request):
    return {'mainmenu': menu(request)}