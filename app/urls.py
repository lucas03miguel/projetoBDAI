from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('login', views.login, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('registo', views.registo, name='registo'),



    path('procurar', views.procurar, name='procurar'),
    path('minhas_playlists', views.minhas_playlists, name='minhas_playlists'),
    path('pesquisar_musicas', views.pesquisar_musicas, name='pesquisar_musicas'),
    path('top10', views.top10, name='top10'),
    
    
    
    path('adicionar_artista', views.adicionar_artista, name='adicionar_artista'),
    path('adicionar_musica', views.adicionar_musica, name='adicionar_musica'),
    path('adicionar_playlist', views.adicionar_playlist, name='adicionar_playlist'),
    path('adicionar_album', views.adicionar_album, name='adicionar_album'),
]