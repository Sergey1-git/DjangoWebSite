from django.urls import path, include

from .import views

app_name = "basket"

urlpatterns = [
    path('basket/', views.basket, name='basket'),

]