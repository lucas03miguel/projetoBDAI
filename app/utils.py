from .models import Consumidor, Artista, Administrador
 

# Função para verificar o tipo do usuário (artista, consumidor, administrador)
def verificar_tipo_usuario(user_id):
    try:
        if Artista.objects.filter(utilizador_user_id=user_id).exists():
            return 'artista'
        
        if Consumidor.objects.filter(utilizador_user_id=user_id).exists():
            return 'consumidor'
        
        if Administrador.objects.filter(utilizador_user_id=user_id).exists():
            return 'administrador'

        return 'desconhecido'

    except Exception as e:
        return 'desconhecido'