
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_playlistmusic_playlist_playlist'),
    ]


    migrations.CreateModel(
        name='PlaylistMusic',
        fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('music_ismn', models.ForeignKey(db_column='music_ismn', on_delete=django.db.models.deletion.PROTECT, to='app.music')),
            ('playlist_playlist', models.ForeignKey(db_column='playlist_playlist_id', on_delete=django.db.models.deletion.PROTECT, to='app.playlist')),
        ],
        options={
            'unique_together': {('playlist_playlist', 'music_ismn')},
        },
    ),