from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Genero(models.Model):
    id_genero = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = 'genero'

class Anime(models.Model):
    id_anime = models.AutoField(primary_key=True)
    nombre_anime = models.CharField(max_length=45)
    genero_id_genero = models.ForeignKey('Genero', models.DO_NOTHING, db_column='genero_id_genero')
    image = models.CharField(max_length=200)
    video = models.CharField(max_length=200)
    rating = models.IntegerField(default=0)
    fecha_ingreso = models.DateField(null=True, blank=True)
    tipo = models.CharField(max_length=45)
    estado = models.CharField(max_length=45)

    def __str__(self):
        return self.nombre_anime
    
    @property
    def ano(self):
        return self.fecha_ingreso.year

    class Meta:
        managed = False
        db_table = 'anime'


class Favorito(models.Model):
    id_favorito = models.AutoField(primary_key=True)
    auth_user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='auth_user_id')
    anime_id_anime = models.ForeignKey(Anime, models.DO_NOTHING, db_column='anime_id_anime')
    es_favorito = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'favorito'


class Personaje(models.Model):
    id_personaje = models.AutoField(primary_key=True)
    nombre_personaje = models.CharField(max_length=45)
    anime_id_anime = models.ForeignKey(Anime, models.DO_NOTHING, db_column='anime_id_anime', related_name='personajes')
    descripcion = models.CharField(max_length=200)
    imagen = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre_personaje + '-' + self.anime_id_anime.nombre_anime

    class Meta:
        managed = False
        db_table = 'personaje'
