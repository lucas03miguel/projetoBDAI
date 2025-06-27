from django.contrib import admin
from .models import (
    Utilizador, Administrador, Artista, Consumidor, Album, Music,
    ArtistaMusic, AlbumMusic, Atividade, Playlist, PlaylistMusic, Top10
)


@admin.register(Utilizador)
class UtilizadorAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'nome', 'idade', 'mail')
    search_fields = ('nome', 'mail')

@admin.register(Administrador)
class AdministradorAdmin(admin.ModelAdmin):
    list_display = ('utilizador_user',)

@admin.register(Artista)
class ArtistaAdmin(admin.ModelAdmin):
    list_display = ('nome_artistico', 'pais_origem', 'administrador_utilizador_user')

@admin.register(Consumidor)
class ConsumidorAdmin(admin.ModelAdmin):
    list_display = ('utilizador_user',)

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'release_date', 'artista_utilizador_user')
    search_fields = ('titulo',)

@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = ('ismn', 'titulo', 'genero', 'release_date', 'duracao', 'artista_que_publicou')
    search_fields = ('titulo', 'genero')

@admin.register(ArtistaMusic)
class ArtistaMusicAdmin(admin.ModelAdmin):
    list_display = ('artista_utilizador_user', 'music_ismn')

@admin.register(AlbumMusic)
class AlbumMusicAdmin(admin.ModelAdmin):
    list_display = ('album_id', 'music_ismn')

@admin.register(Atividade)
class AtividadeAdmin(admin.ModelAdmin):
    list_display = ('music_ismn', 'play_count', 'last_time', 'consumidor_utilizador_user')

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('playlist_id', 'nome', 'data_criacao', 'consumidor_utilizador_user')

@admin.register(PlaylistMusic)
class PlaylistMusicAdmin(admin.ModelAdmin):
    list_display = ('playlist_playlist', 'music_ismn')

@admin.register(Top10)
class Top10Admin(admin.ModelAdmin):
    list_display = ('playlist_playlist', 'consumidor_utilizador_user')