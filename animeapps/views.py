from django.shortcuts import render, redirect
from .models import Genero, Personaje, Anime, Favorito
from django.db.models.functions import ExtractYear
from django.db.models import Q
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from datetime import datetime

# Create your views here.

def animes(request):
    animex = Anime.objects.all().order_by('nombre_anime')
    now = datetime.now()
    animepuntuacion = Anime.objects.order_by('-rating')[:5]
    return render(request, 'index.html', {
        'animes' : animex,
        'animepun': animepuntuacion,
        'now' : now
    })

# def animes(request):
#     animex = Anime.objects.order_by('nombre_anime')
#     return render(request, 'index.html', {'animes': animex})

def info_anime(request, id):
    anime = Anime.objects.filter(id_anime=id).first()
    personajes = Personaje.objects.filter(anime_id_anime=anime)
    if request.user.is_authenticated:
        favorito = Favorito.objects.filter(auth_user_id=request.user, anime_id_anime=anime).first()
        if request.method == 'POST':
            es_favorito = request.POST.get('es_favorito',False)
            puntuacion_actual = anime.rating
            if es_favorito == 'True' and not favorito:
                anime.rating = puntuacion_actual+ 1
                anime.save()
                Favorito.objects.create(auth_user_id=request.user, anime_id_anime=anime, es_favorito=True)
            elif es_favorito == 'False' and favorito:
                puntuacion_actual = anime.rating
                if puntuacion_actual > 0:
                    anime.rating = puntuacion_actual - 1
                    anime.save()
                favorito.delete()
            elif es_favorito == 'True' and favorito:
                favorito.es_favorito = True
                favorito.save()
                Favorito.objects.create(auth_user_id=request.user, anime_id_anime=anime, es_favorito=es_favorito)
            return redirect('info_anime', id=anime.id_anime)
    else:
        favorito = Favorito.objects.filter(anime_id_anime=anime).first()
    anios = Anime.objects.dates('fecha_ingreso', 'year', order='DESC')
    return render(request, 'info-anime.html', {
        'anime': anime,
        'personajes': personajes,
        'favorito': favorito,
        'anios': anios
    })

def generos(request):
    generox = Genero.objects.all()
    return render(request,'index.html', {
        'generos' : generox
    })

def create_genero(request):
    if request.method == 'POST':
        
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')

        genero=Genero.objects.create(
            
            nombre = nombre,
            descripcion = descripcion
        )
        genero.save
        return redirect('/')
    return render(request, 'create-genero.html')

@user_passes_test(lambda user: user.is_superuser, login_url='login')
def create_anime(request):
    if request.method == 'POST':
       
        nombre = request.POST.get('nombre')
        genero_id = request.POST.get('genero')
        genero = Genero.objects.get(id_genero=genero_id)
        image = request.POST.get('imagen')
        fecha = request.POST.get('fecha')

        anime = Anime.objects.create(
           
            nombre_anime=nombre,
            fecha_ingreso = fecha,
            genero_id_genero=genero,
            image=image
        )
        anime.save()
        return redirect('animes')

    generos = Genero.objects.all()
    return render(request, 'create-anime.html', {'generos': generos})

def create_personaje(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        anime_id = request.POST.get('anime')
        anime = Anime.objects.get(id_anime=anime_id)
        imagen = request.POST.get('imagen')
        descripcion = request.POST.get('descripcion')
        
        personaje = Personaje.objects.create(

            nombre_personaje = nombre,
            anime_id_anime = anime,
            descripcion = descripcion,
            imagen = imagen,
        )
        personaje.save()
        return redirect('/')
    
    animex = Anime.objects.all()
    return render(request, 'create-personaje.html', {'anime': animex})

def eliminar(request):
    if request.method == 'POST':
        if 'eliminar_anime' in request.POST:
            anime_id = request.POST['eliminar_animex']
            anime = Anime.objects.get(id_anime=anime_id)
            anime.delete()
            return redirect('/')
        elif 'eliminar_personaje' in request.POST:
            personaje_id = request.POST['eliminar_personajex']
            personaje = Personaje.objects.get(id_personaje=personaje_id)
            personaje.delete()
            return redirect('/')
    else:
        animes = Anime.objects.all()
        personajes = Personaje.objects.all()
        return render(request, 'eliminar.html', {'animes': animes, 'personajes': personajes})


def editar(request):
    if request.method == 'POST':
        anime_id = request.POST.get('anime')
        anime = Anime.objects.get(id_anime=anime_id)
        anime.nombre_anime = request.POST.get('nombre_anime')
        genero_id = request.POST.get('genero')
        genero = Genero.objects.get(id_genero=genero_id)
        anime.genero_id_genero = genero
        anime.image = request.POST.get('imagen')
        anime.save()
        return redirect('/')
    else:
        animes = Anime.objects.all()
        generos = Genero.objects.all()
        return render(request, 'editar.html', {'animes': animes, 'generos': generos})


def allanime(request):
    listaanos = list(range(1990, 2024))
    listaanos = sorted(listaanos, reverse=True)
    if request.method == 'POST':
        year = request.POST.get('year')
        genero = request.POST.get('genero')
        estado = request.POST.get('estado')
        tipo = request.POST.get('tipo')
        # construir la consulta base
        animes = Anime.objects.all()
        # agregar el filtro de año
        if year:
            animes = animes.filter(fecha_ingreso__year=year)
        # agregar el filtro de género
        if genero:
            animes = animes.filter(genero_id_genero=genero)
        if estado:
            animes = animes.filter(estado=estado)
        if tipo:
            animes = animes.filter(tipo=tipo)
        generos = Genero.objects.all()
        return render(request, 'all-anime.html', {'animes': animes, 'generos': generos,'listaanos' : listaanos})
    else: 
        animes = Anime.objects.all()
        generos = Genero.objects.all()
        animes = Anime.objects.all().prefetch_related('personajes')
        for anime in animes:
            anime.num_personajes = anime.personajes.count()
        anios = Anime.objects.dates('fecha_ingreso', 'year', order='DESC')
        return render(request, 'all-anime.html', {'animes': animes, 'generos': generos,'anios': anios,'listaanos' : listaanos})
        #Entender este codigo.

def pruebas(request):
    #animeq = Anime.objects.annotate(num_personajes=Count('personajes')).values('nombre_anime', 'num_personajes')
    #return render(request, 'pruebas.html', {'animes': animeq})
    animex = Anime.objects.all().prefetch_related('personajes')
    for anime in animex:
        anime.num_personajes = anime.personajes.count()
    return render(request, 'pruebas.html', {'animex': animex})


def tienda(request):
    return render(request, 'tienda.html')

def exit(request):
    logout(request)
    return redirect('animes')
    
   