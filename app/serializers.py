from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(read_only=True)
    mail = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    nome = serializers.CharField(
        max_length=255,
        min_length=3,
        error_messages={
            "max_length": "O nome deve ter no máximo 255 caracteres.",
            "min_length": "O nome deve ter pelo menos 3 caracteres.",
        }
    )

    idade = serializers.IntegerField(
        min_value=0,
        max_value=150,
        error_messages={
            "min_value": "A idade deve ser um número positivo.",
            "max_value": "A idade não pode ser superior a 150 anos.",
        }
    )

    morada = serializers.CharField(
        max_length=512,
        min_length=3,
        error_messages={
            "max_length": "A morada deve ter no máximo 512 caracteres.",
            "min_length": "A morada deve ter pelo menos 3 caracteres.",
        }
    )
    


class ArtistSerializer(serializers.Serializer):
    nome_artistico = serializers.CharField(
        max_length=255,
        min_length=3,
        error_messages={
            "max_length": "O nome deve ter no máximo 255 caracteres.",
            "min_length": "O nome deve ter pelo menos 3 caracteres.",
        }
    )

    pais_origem = serializers.CharField(
        max_length=255,
        min_length=3,
        error_messages={
            "max_length": "O país de origem deve ter no máximo 255 caracteres.",
            "min_length": "O país de origem deve ter pelo menos 3 caracteres.",
        }
    )
    
