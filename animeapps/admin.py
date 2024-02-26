from django.contrib import admin
from .models import Anime,Genero,Personaje,Favorito
# Register your models here.


admin.site.register(Genero)
admin.site.register(Anime)
admin.site.register(Personaje)
admin.site.register(Favorito)