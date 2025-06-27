from django.db import models


class Utilizador(models.Model):
    user_id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=512)
    idade = models.IntegerField()
    morada = models.CharField(max_length=512)
    mail = models.CharField(unique=True, max_length=512)
    password = models.CharField(max_length=512)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Utilizadores"


class Administrador(models.Model):
    utilizador_user = models.OneToOneField('Utilizador', models.PROTECT, primary_key=True)

    def __str__(self):
        return f"Administrador {self.utilizador_user.nome}"

    class Meta:
        verbose_name_plural = "Administradores"


class Artista(models.Model):
    nome_artistico = models.CharField(max_length=512)
    pais_origem = models.CharField(max_length=512)
    administrador_utilizador_user = models.ForeignKey('Administrador', models.PROTECT)
    utilizador_user = models.OneToOneField('Utilizador', models.PROTECT, primary_key=True)

    def __str__(self):
        return f"Artista {self.nome_artistico}"

    class Meta:
        verbose_name_plural = "Artistas"


class Consumidor(models.Model):
    utilizador_user = models.OneToOneField('Utilizador', models.PROTECT, primary_key=True)

    def __str__(self):
        return f"Consumidor {self.utilizador_user.nome}"

    class Meta:
        verbose_name_plural = "Consumidores"


class Album(models.Model):
    id = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=512)
    release_date = models.DateField()
    artista_utilizador_user = models.ForeignKey('Artista', models.PROTECT)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name_plural = "Álbuns"


class Music(models.Model):
    ismn = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=512)
    genero = models.CharField(max_length=512)
    release_date = models.DateField()
    duracao = models.CharField(max_length=512)
    artista_que_publicou = models.IntegerField()

    def __str__(self):
        return f"{self.titulo} - {self.artista_que_publicou}"

    class Meta:
        verbose_name_plural = "Músicas"


class ArtistaMusic(models.Model):
    artista_utilizador_user = models.ForeignKey('Artista', on_delete=models.PROTECT)
    music_ismn = models.ForeignKey('Music', on_delete=models.PROTECT, db_column='music_ismn')

    class Meta:
        unique_together = (('artista_utilizador_user', 'music_ismn'),)
        verbose_name_plural = "Músicas dos artistas"

    def __str__(self):
        return f"{self.artista_utilizador_user.nome_artistico} participou na música com ISMN {self.music_ismn}"


class AlbumMusic(models.Model):
    album_id = models.ForeignKey(Album, models.PROTECT, db_column='album_id')
    music_ismn = models.ForeignKey(Music, models.PROTECT, db_column='music_ismn')

    class Meta:
        unique_together = (('album_id', 'music_ismn'),)
        verbose_name_plural = "Músicas dos álbuns"


class Atividade(models.Model):
    play_count = models.IntegerField()
    last_time = models.DateField()
    music_ismn = models.OneToOneField('Music', models.PROTECT, db_column='music_ismn', primary_key=True)
    consumidor_utilizador_user = models.ForeignKey('Consumidor', models.PROTECT)

    def __str__(self):
        return f"{self.music_ismn} tocada {self.play_count} vezes"

    class Meta:
        unique_together = (('music_ismn', 'consumidor_utilizador_user'),)
        verbose_name_plural = "Atividades"


class Playlist(models.Model):
    playlist_id = models.AutoField(primary_key=True)
    data_criacao = models.DateField(auto_now_add=True)
    nome = models.CharField(max_length=512)
    consumidor_utilizador_user = models.ForeignKey(Consumidor, models.PROTECT)

    def __str__(self):
        return f"Playlist: {self.nome}"

    class Meta:
        verbose_name_plural = "Playlists"


class PlaylistMusic(models.Model):
    playlist_playlist = models.ForeignKey('Playlist', models.PROTECT, db_column='playlist_playlist_id')
    music_ismn = models.ForeignKey('Music', models.PROTECT, db_column='music_ismn')

    class Meta:
        unique_together = (('playlist_playlist', 'music_ismn'),)
        verbose_name_plural = "Músicas das playlists"


class Top10(models.Model):
    playlist_playlist = models.OneToOneField(Playlist, models.PROTECT)
    consumidor_utilizador_user = models.OneToOneField(Consumidor, models.PROTECT, primary_key=True)

    def __str__(self):
        return f"Top 10 de {self.consumidor_utilizador_user.utilizador_user.nome}"

    class Meta:
        verbose_name_plural = "Top 10s"