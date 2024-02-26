from django.urls import path,include
from . import views


urlpatterns = [

    path('',views.animes, name='animes'),
    path('info_anime/<int:id>',views.info_anime, name='info_anime'),
    path('create_anime/', views.create_anime, name='crear_anime'),
    path('create_genero/', views.create_genero, name='crear_genero'),
    path('create_personaje/', views.create_personaje, name='crear_personaje'),
    path('eliminar/', views.eliminar, name='eliminar'),
    path('editar/', views.editar, name='editar'),
    path('allanime/', views.allanime, name='allanime'),
    path('pruebas/', views.pruebas, name='pruebas'),
    path('accounts/', include('django.contrib.auth.urls'), name='login'),
    path('logout/', views.exit, name='exit'),
    path('tienda/',views.tienda, name= 'tienda'),
    

]