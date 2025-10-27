from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index,name='home' ),
    path('add_product/', views.add_product, name='add_product'),
    path('homemade_flowers/', views.homemade_flowers, name='homemade_flowers'),
    path('garden_flowers/', views.garden_flowers, name='garden_flowers'),
    path('post/<int:id>/', views.show_post, name='show_post'),
    path('contact/', views.contact, name='contact'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #Для отображения в режиме отладки