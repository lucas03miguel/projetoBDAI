from django.db.models import Q
from django.db import transaction
from django.template import loader
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password, check_password

import json
from .utils import *
from .models import *
from datetime import timedelta, datetime
from app.serializers import ArtistSerializer, UserSerializer


def logout_user(request):
    logout(request)
    request.session.flush()
    return redirect('/app/login')



# View para adicionar utilizador
def registo(request):
    template = loader.get_template('registo.html')
    context = {}
    

    if request.method == 'POST':
        payload = request.POST
        serializer = UserSerializer(data=payload)

        if not serializer.is_valid():
            erros = []
            for field, errors in serializer.errors.items():
                for error in errors:
                    erros.append(f"{field.capitalize()}: {error}")

            context = {
                'status': 'error', 
                'errors': erros
            }

            return HttpResponse(template.render(context, request))
        
        payload = serializer.validated_data
        try:
            with transaction.atomic():

                if Utilizador.objects.filter(mail=payload['mail']).exists():
                    context = {
                        'status': 'error',
                        'errors': ['Email já registado']
                    }
                    return HttpResponse(template.render(context, request))

                user = Utilizador.objects.create(
                    mail=payload['mail'],
                    password=make_password(payload['password']),
                    nome=payload['nome'],
                    idade=payload['idade'],
                    morada=payload['morada']
                )
                
                Consumidor.objects.create(
                    utilizador_user_id=user.user_id
                )
                
                context = {
                    'status': 'success',
                    'results': str(user.user_id)
                }

        except Exception as e:
            print(e)
            context = {
                'status': 'error',
                'errors': [str(e)]
            }
    
    return HttpResponse(template.render(context, request))



# View para adicionar artista
def adicionar_artista(request):
    if 'user_id' not in request.session:
        messages.error(request, 'Por favor faça login.')
        return redirect('/app/login')
    
    elif verificar_tipo_usuario(request.session['user_id']) != 'administrador':
        messages.error(request, 'Apenas administradores podem adicionar artistas.')
        return redirect('/app/login')
    
    template = loader.get_template('adicionar_artista.html')
    context = {}
    

    if request.method == 'POST':
        payload_aux = request.POST
        serializer = UserSerializer(data=payload_aux)

        if not serializer.is_valid():
            erros = []
            for field, errors in serializer.errors.items():
                for error in errors:
                    erros.append(f"{field.capitalize()}: {error}")

            context = {
                'status': 'error', 
                'errors': erros
            }
            
            return HttpResponse(template.render(context, request))
        
        serializer_aux = serializer
        serializer = ArtistSerializer(data=payload_aux)
        if not serializer.is_valid():
            erros = []
            for field, errors in serializer.errors.items():
                for error in errors:
                    erros.append(f"{field.capitalize()}: {error}")

            context = {
                'status': 'error', 
                'errors': erros
            }
            
            return HttpResponse(template.render(context, request))
        
        payload = {}
        for field, value in serializer_aux.validated_data.items():
            payload.update({field: value}) 
        
        for field, value in serializer.validated_data.items():
            payload.update({field: value})

        try:
            with transaction.atomic(): # Garante que todas as operações são executadas como um só

                if Utilizador.objects.filter(mail=payload['mail']).exists():
                    context = {
                        'status': 'error',
                        'errors': ['Email já registado']
                    }
                    return HttpResponse(template.render(context, request))

                user = Utilizador.objects.create(
                    mail=payload['mail'],
                    password=make_password(payload['password']),
                    nome=payload['nome'],
                    idade=payload['idade'],
                    morada=payload['morada']
                )
                
                Artista.objects.create(
                    nome_artistico=payload['nome_artistico'],
                    pais_origem=payload['pais_origem'],
                    administrador_utilizador_user_id=request.session['user_id'],
                    utilizador_user_id=user.user_id
                )             

                context = {
                    'status': 'success',
                    'results': str(user.user_id)
                }

        except Exception as e:
            print(e)
            context = {
                'status': 'error',
                'errors': [e]
            }
    
    return HttpResponse(template.render(context, request))



# View para fazer login
def login(request):
    template = loader.get_template('login.html')
    context = {}

    if request.method == 'POST' and request.POST.get('_method') == 'PUT':
        payload = request.POST        
        mail = payload.get('email')
        password = payload.get('password')

        if not mail or not password:
            context = {
                'status': 'error',
                'errors': 'Os campos email e password são obrigatórios.'
            }
            return HttpResponse(template.render(context, request))
        
        try:
            user = Utilizador.objects.filter(mail=mail).first()

            if user:    
                user_type = verificar_tipo_usuario(user.user_id)

                if check_password(password, user.password):
                    request.session['user_id'] = user.user_id

                    context = {
                        'status': 'success',
                        'user': user_type
                    }

                    return redirect('/app/index')
                
                elif user_type == 'administrador' and user.password == password: #teve que ser assim porque o admin é inserido manualmente
                    request.session['user_id'] = user.user_id

                    context = {
                        'status': 'success',
                        'user': user_type
                    }

                    return redirect('/app/index')
                    
                else:
                    context = {
                        'status': 'error',
                        'errors': 'Credenciais inválidas'
                    }

            else:
                context = {
                    'status': 'error',
                    'errors': 'Utilizador não encontrado'
                }

        except Exception as e:
            print(e)
            context = {
                'status': 'internal_error',
                'errors': str(e)
            }

    return HttpResponse(template.render(context, request))



# View principal (index)
def index(request):
    if 'user_id' not in request.session:
        messages.error(request, 'Por favor faça login.')
        return redirect('/app/login')
    
    template = loader.get_template('index.html')

    count = 0
    for i in Atividade.objects.all():
        count += i.play_count
    
    context = {
        'num_artistas': Artista.objects.all().count(),
        'num_consumidores': Consumidor.objects.all().count(),
        'num_administradores': Administrador.objects.all().count(),
        'num_musicas': Music.objects.all().count(),
        'num_artista_music': ArtistaMusic.objects.all().count(),
        'num_playlists': Playlist.objects.all().count(),
        'num_playlist_musicas': PlaylistMusic.objects.all().count(),
        'num_albuns': Album.objects.all().count(),
        'num_reproducoes': count,
        'nome': Utilizador.objects.get(user_id=request.session['user_id']).nome,
        'type': verificar_tipo_usuario(request.session['user_id'])
    }
    
    return HttpResponse(template.render(context, request))



# View para adicionar música
def adicionar_musica(request):
    if 'user_id' not in request.session:
        messages.error(request, 'Por favor faça login.')
        return redirect('/app/login')
    
    elif verificar_tipo_usuario(request.session['user_id']) != 'artista':
        messages.error(request, 'Apenas artistas podem adicionar músicas.')
        return redirect('/app/login')
    
    template = loader.get_template('adicionar_musica.html')
    context = {
        'artistas': Artista.objects.all(),
        'usuario': request.session['user_id']
    }

    if request.method == 'POST':
        payload = request.POST
        try:
            with transaction.atomic():

                publisher_id = int(request.session['user_id'])
                featured_artists_ids = payload.getlist('artistas_participantes')

                existing_music = Music.objects.filter(
                    titulo=payload.get('titulo'),
                    genero=payload.get('genero'),
                    duracao=payload.get('duracao'),
                    artista_que_publicou=publisher_id
                ).first()

                if existing_music:
                    existing_features = ArtistaMusic.objects.filter(
                        music_ismn=existing_music
                    ).values_list('artista_utilizador_user_id', flat=True)
                    
                    existing_features_set = set(existing_features)
                    new_features_set = set(map(int, featured_artists_ids))

                    new_features_set.add(publisher_id)

                    if existing_features_set == new_features_set:
                        context = {
                            'status': 'error',
                            'errors': ['Já existe uma música com os mesmos campos e os mesmos artistas participantes.']
                        }

                        return HttpResponse(template.render(context, request))

                music = Music.objects.create(
                    titulo=payload.get('titulo'),
                    genero=payload.get('genero'),
                    release_date=datetime.now(),
                    duracao=payload.get('duracao'),
                    artista_que_publicou=publisher_id
                )

                ArtistaMusic.objects.create(
                    artista_utilizador_user_id=publisher_id,
                    music_ismn=music
                )

                for artist_id in featured_artists_ids:
                    ArtistaMusic.objects.create(
                        artista_utilizador_user_id=int(artist_id),
                        music_ismn=music
                    )

                context = {
                    'status': 'success', 
                    'results': music, 
                    'usuario': request.session['user_id']
                }

        except Exception as e:
            print(e)
            context = {
                'status': 'error', 
                'errors': [str(e)], 
                'usuario': request.session['user_id']
            }

    return HttpResponse(template.render(context, request))



# View para adicionar playlist
def adicionar_playlist(request):
    if 'user_id' not in request.session:
        messages.error(request, 'Por favor faça login.')
        return redirect('/app/login')
    
    elif verificar_tipo_usuario(request.session['user_id']) != 'consumidor':
        messages.error(request, 'Apenas consumidores podem aceder a esta página.')
        return redirect('/app/login')
    
    template = loader.get_template('adicionar_playlist.html')

    if request.method == 'POST':
        try:
            with transaction.atomic():
                payload = request.POST

                titulo = payload.get('titulo', '').strip()
                musicas_ids = payload.get('musicas', '[]')
                
                try:
                    musicas_ids = json.loads(musicas_ids)  # Carrega a lista de ISMNs
                except json.JSONDecodeError:
                    musicas_ids = []

                if musicas_ids == []:
                    context = {
                        'status': 'error', 
                        'errors': ['Por favor selecione pelo menos uma música.']
                    }
                    return HttpResponse(template.render(context, request))

                # Cria nova playlist
                playlist = Playlist.objects.create(
                    nome=titulo,
                    consumidor_utilizador_user_id=request.session['user_id']
                )


                for musica_ismn in musicas_ids:
                    musica = Music.objects.get(ismn=musica_ismn)
                    
                    PlaylistMusic.objects.create(
                        playlist_playlist=playlist,
                        music_ismn=musica
                    )


                context = {
                    'status': 'success',
                    'results': playlist.playlist_id
                }

                return HttpResponse(template.render(context, request))
        except Exception as e:
            print(e)
            context = {
                'status': 'error',
                'errors': [str(e)]
            }
    

    todas_musicas = Music.objects.all()
    context = {
        'musicas': todas_musicas
    }

    return HttpResponse(template.render(context, request))



# View para adicionar albuns
def adicionar_album(request):
    if 'user_id' not in request.session:
        messages.error(request, 'Por favor faça login.')
        return redirect('/app/login')
    
    elif verificar_tipo_usuario(request.session['user_id']) != 'artista':
        messages.error(request, 'Apenas consumidores podem aceder a esta página.')
        return redirect('/app/login')
    

    template = loader.get_template('adicionar_album.html')
    discografia = list(Music.objects.values("ismn", "titulo"))
    
    context = {
        "discografia": json.dumps(discografia)
    }

    if request.method == 'POST':
        payload = request.POST

        try:
            with transaction.atomic():
                album = Album.objects.create(
                    titulo=payload['nome_album'],
                    release_date=datetime.now(),
                    artista_utilizador_user_id=request.session['user_id']
                )

                num_musicas = int(payload['numero_musicas'])
                for i in range(1, num_musicas + 1):
                    musica_id = payload.get(f'musica_discografia_{i}')

                    if musica_id:
                        # Musica existente
                        music = Music.objects.get(ismn=musica_id)

                        AlbumMusic.objects.create(
                            album_id=album, 
                            music_ismn=music
                        )
                    else:
                        # Nova música

                        titulo = payload[f'titulo_{i}']
                        genero = payload[f'genero_{i}']
                        duracao = payload[f'duracao_{i}']
                        artista = request.session['user_id']
                        
                        music = Music.objects.filter(
                            titulo=titulo,
                            genero=genero,
                            duracao=duracao,
                            artista_que_publicou=artista
                        ).first()

                        if music:
                            context = {
                                'status': 'error',
                                'errors': [f'Música {i} já existe']
                            }

                            return HttpResponse(template.render(context, request))
                        else:
                            # Criar a nova música
                            nova_musica = Music.objects.create(
                                titulo=titulo,
                                genero=genero,
                                release_date=datetime.now(),
                                duracao=duracao,
                                artista_que_publicou=artista
                            )

                            ArtistaMusic.objects.create(
                                artista_utilizador_user_id=artista,
                                music_ismn=nova_musica
                            )

                            AlbumMusic.objects.create(album_id=album, music_ismn=nova_musica)
                
                context = {
                    'status': 'success',
                    'results': album.id
                }

        except Exception as e:
            print(e)
            context = {
                'status': 'error',
                'errors': ["Erro no servidor"]
            }
    
    return HttpResponse(template.render(context, request))



def pesquisar_musicas(request):
    query = request.GET.get('q', '').strip()
    musicas = []
    if query:
        musicas = Music.objects.filter(
            Q(titulo__icontains=query) | 
            Q(genero__icontains=query) | 
            Q(artista_que_publicou__in=Artista.objects.filter(nome_artistico__icontains=query).values('utilizador_user_id'))
        ).values('ismn', 'titulo')
    
    return JsonResponse({"musicas": list(musicas)}, safe=False)



# View para procurar música
def procurar(request):
    if 'user_id' not in request.session:
        messages.error(request, 'Por favor faça login.')
        return redirect('/app/login')

    elif verificar_tipo_usuario(request.session['user_id']) != 'consumidor':
        messages.error(request, 'Apenas consumidores podem aceder a esta página.')
        return redirect('/app/login')

    template = loader.get_template('procurar.html')
    query = request.GET.get('q', '').strip()
    filtro = request.GET.get('filtro', 'tudo')
    resultados = []
    context = {}

    if query:
        if filtro in ['tudo', 'artistas']:
            artistas = Artista.objects.filter(nome_artistico__icontains=query)
            for artista in artistas:
                resultados.append({
                    'nome': artista.nome_artistico,
                    'tipo': 'Artista',
                    'id': artista.utilizador_user_id
                })

        if filtro in ['tudo', 'musicas']:
            musicas = Music.objects.filter(titulo__icontains=query)
            for musica in musicas:
                resultados.append({
                    'nome': musica.titulo,
                    'tipo': 'Música',
                    'id': musica.ismn
                })

        if filtro in ['tudo', 'playlists']:
            playlists = Playlist.objects.filter(nome__icontains=query)
            for playlist in playlists:
                resultados.append({
                    'nome': playlist.nome,
                    'tipo': 'Playlist',
                    'id': playlist.playlist_id
                })

        if filtro in ['tudo', 'albuns']:
            albuns = Album.objects.filter(titulo__icontains=query)
            for album in albuns:
                resultados.append({
                    'nome': album.titulo,
                    'tipo': 'Álbum',
                    'id': album.id
                })
        
        context.update({'resultados': resultados})
    else:
        user_id = request.GET.get('user_id')
        musica_id = request.GET.get('musica_id')
        album_id = request.GET.get('album_id')
        playlist_id = request.GET.get('playlist_id')
        musica_id_reproduzir = request.GET.get('musica_id_reproduzir')
        playlist_id_reproduzir = request.GET.get('playlist_id_reproduzir')
        album_id_reproduzir = request.GET.get('album_id_reproduzir')
        

        if user_id:
            artista_selecionado = Artista.objects.get(utilizador_user_id=user_id)
            
            context = {
                'artista_selecionado': artista_selecionado,
                'num_albuns': Album.objects.filter(artista_utilizador_user_id=user_id).count(),
                'num_musicas': ArtistaMusic.objects.filter(artista_utilizador_user_id=user_id).count(),
                'resultados': [{
                    'nome': artista_selecionado.nome_artistico,
                    'tipo': 'Artista',
                    'id': artista_selecionado.utilizador_user_id
                }]
            }

        elif musica_id:
            musica_selecionada = Music.objects.get(ismn=musica_id)
            context = {
                'musica_selecionada': musica_selecionada,
                'nome_artista': Artista.objects.get(utilizador_user_id=musica_selecionada.artista_que_publicou).nome_artistico,
                'resultados': [{
                    'nome': musica_selecionada.titulo,
                    'tipo': 'Música',
                    'id': musica_selecionada.ismn
                }]
            }

            if musica_id_reproduzir:
                consumidor = Consumidor.objects.get(utilizador_user_id=request.session['user_id'])
                musica = Music.objects.get(ismn=musica_id_reproduzir)

                atividade, created = Atividade.objects.get_or_create(
                    music_ismn=musica,
                    consumidor_utilizador_user=consumidor,
                    defaults={'play_count': 0, 'last_time': datetime.now()}
                )

                atividade.play_count += 1
                atividade.last_time = datetime.now()
                atividade.save()
                context.update({'status': 'success', 'results': 'A reproduzir música!'})
        

        elif album_id:
            album_selecionado = Album.objects.get(id=album_id)


            duracao_total = 0
            musicas_album = AlbumMusic.objects.filter(album_id=album_selecionado)
            for musica in musicas_album:
                duracao = musica.music_ismn.duracao.split(":")
                duracao_musica = 3600 * int(duracao[0]) + 60 * int(duracao[1]) + int(duracao[2])
                duracao_total += duracao_musica

            duracao_total = str(timedelta(seconds=duracao_total))
            context = {
                'album_selecionado': album_selecionado,
                'numero_musicas': AlbumMusic.objects.filter(album_id=album_selecionado).count(),
                'duracao': duracao_total,
                'resultados': [{
                    'nome': album_selecionado.titulo,
                    'tipo': 'Álbum',
                    'id': album_selecionado.id
                }]
            }

            if album_id_reproduzir:
                album = Album.objects.get(id=album_id_reproduzir)
                
                musicas_relacionadas = Music.objects.filter(
                    ismn__in=AlbumMusic.objects.filter(
                        album_id=album
                    ).values('music_ismn')
                )
                

                consumidor = Consumidor.objects.get(utilizador_user_id=request.session['user_id'])
                for musica in musicas_relacionadas:
                    atividade, created = Atividade.objects.get_or_create(
                        music_ismn=musica,
                        consumidor_utilizador_user=consumidor,
                        defaults={'play_count': 0, 'last_time': datetime.now()}
                    )

                    atividade.play_count += 1
                    atividade.last_time = datetime.now()
                    atividade.save()

                context.update({'status': 'success', 'results': 'A reproduzir playlist!'})


        elif playlist_id:
            playlist_selecionada = Playlist.objects.get(playlist_id=playlist_id)

            duracao_total = 0
            musicas_playlist = PlaylistMusic.objects.filter(playlist_playlist=playlist_selecionada)
            for musica in musicas_playlist:
                duracao = musica.music_ismn.duracao.split(":")
                duracao_musica = 3600 * int(duracao[0]) + 60 * int(duracao[1]) + int(duracao[2])
                duracao_total += duracao_musica

            duracao_total = str(timedelta(seconds=duracao_total))
            context = {
                'playlist_selecionada': playlist_selecionada,
                'numero_musicas': PlaylistMusic.objects.filter(playlist_playlist=playlist_selecionada).count(),
                'duracao': duracao_total,
                'resultados': [{
                    'nome': playlist_selecionada.nome,
                    'tipo': 'Playlist',
                    'id': playlist_selecionada.playlist_id
                }]
            }
    
            if playlist_id_reproduzir:
                playlist = Playlist.objects.get(playlist_id=playlist_id_reproduzir)
                
                musicas_relacionadas = Music.objects.filter(
                    ismn__in=PlaylistMusic.objects.filter(
                        playlist_playlist=playlist
                    ).values('music_ismn')
                )
                

                consumidor = Consumidor.objects.get(utilizador_user_id=request.session['user_id'])
                for musica in musicas_relacionadas:
                    atividade, created = Atividade.objects.get_or_create(
                        music_ismn=musica,
                        consumidor_utilizador_user=consumidor,
                        defaults={'play_count': 0, 'last_time': datetime.now()}
                    )

                    atividade.play_count += 1
                    atividade.last_time = datetime.now()
                    atividade.save()

                context.update({'status': 'success', 'results': 'A reproduzir playlist!'})

    return HttpResponse(template.render(context, request))



# View para o top10
def top10(request):
    if 'user_id' not in request.session:
        messages.error(request, 'Por favor faça login.')
        return redirect('/app/login')

    elif verificar_tipo_usuario(request.session['user_id']) != 'consumidor':
        messages.error(request, 'Apenas consumidores podem aceder a esta página.')
        return redirect('/app/login')

    template = loader.get_template('top10.html')
    context = {}

    consumidor = Consumidor.objects.get(utilizador_user_id=request.session['user_id'])
    if request.method == 'POST':
        atividades = Atividade.objects.filter(music_ismn=request.POST.get('music_id'))

        if atividades:
            atividades[0].play_count += 1
            atividades[0].last_time = datetime.now()
            atividades[0].save()

        else:
            Atividade.objects.create(
                music_ismn=Music.objects.get(ismn=request.POST.get('music_id')),
                consumidor_utilizador_user=consumidor,
                play_count=1,
                last_time=datetime.now()
            )

        context.update({'status': 'success', 'results': Music.objects.get(ismn=request.POST.get('music_id')).titulo})


    top_musicas = (
        Atividade.objects.filter(consumidor_utilizador_user=consumidor)
        .order_by('-play_count')[:10]
    )

    top10_musicas = []
    for atividade in top_musicas:
        musica = atividade.music_ismn
        try:
            artista = Artista.objects.get(utilizador_user_id=musica.artista_que_publicou)
            nome_artista = artista.nome_artistico
        except Artista.DoesNotExist:
            nome_artista = "Desconhecido"

        top10_musicas.append({
            'musica': musica.titulo,
            'artista': nome_artista,
            'id': musica.ismn,
            'reproducoes': atividade.play_count
        })


    context.update({'top10': top10_musicas})
    return HttpResponse(template.render(context, request))



# View para ver as minhas playlists
def minhas_playlists(request):
    if 'user_id' not in request.session:
        messages.error(request, 'Por favor faça login.')
        return redirect('/app/login')
    elif verificar_tipo_usuario(request.session['user_id']) != 'consumidor':
        messages.error(request, 'Apenas consumidores podem aceder a esta página.')
        return redirect('/app/login')

    template = loader.get_template('minhas_playlists.html')
    context = {}

    with transaction.atomic():
        try:
            todas_playlists = Playlist.objects.filter(consumidor_utilizador_user=request.session['user_id'])

            if request.method == 'POST':
                payload = request.POST
                playlist_id_post = payload['playlist_id']
                

                if payload['acao'] == 'reproduzir':
                    playlist = Playlist.objects.get(playlist_id=playlist_id_post)
                    
                    musicas_relacionadas = Music.objects.filter(
                        ismn__in=PlaylistMusic.objects.filter(
                            playlist_playlist=playlist
                        ).values('music_ismn')
                    )
                    

                    consumidor = Consumidor.objects.get(utilizador_user_id=request.session['user_id'])
                    for musica in musicas_relacionadas:
                        atividade, created = Atividade.objects.get_or_create(
                            music_ismn=musica,
                            consumidor_utilizador_user=consumidor,
                            defaults={'play_count': 0, 'last_time': datetime.now()}
                        )

                        atividade.play_count += 1
                        atividade.last_time = datetime.now()
                        atividade.save()

                    playlist_tocar = Playlist.objects.get(playlist_id=playlist_id_post).nome
                    context = {
                        'modo_detalhes': True,
                        'playlist': playlist,
                        'musicas': musicas_relacionadas,
                        'todas_playlists': todas_playlists,
                        'status': 'success',
                        'results': f'A reproduzir playlist {playlist_tocar}!'
                    }

                    return HttpResponse(template.render(context, request))

                elif payload['acao'] == 'apagar':
                    try:
                        PlaylistMusic.objects.filter(playlist_playlist=playlist_id_post).delete()
                        Playlist.objects.filter(playlist_id=playlist_id_post).delete()

                        context = {
                            'status': 'success',
                            'results': 'Playlist apagada com sucesso'
                        }
                    except Exception as e:
                        print(e)
                        context = {
                            'status': 'error',
                            'errors': [str(e)]
                        }
            

            playlist_id_get = request.GET.get('playlist_id')
            if playlist_id_get:
                playlist = Playlist.objects.get(playlist_id=playlist_id_get)
                
                musicas_relacionadas = Music.objects.filter(
                    ismn__in=PlaylistMusic.objects.filter(
                        playlist_playlist=playlist
                    ).values('music_ismn')
                )

                context.update({
                    'modo_detalhes': True,
                    'playlist': playlist,
                    'musicas': musicas_relacionadas,
                    'todas_playlists': todas_playlists,
                })

            else:

                context.update({
                    'modo_detalhes': False,
                    'todas_playlists': todas_playlists,
                })
        except Exception as e:
            print(e)
            context = {
                'status': 'error',
                'todas_playlists': todas_playlists,
                'errors': ['Erro no servidor']
            }

    return HttpResponse(template.render(context, request))