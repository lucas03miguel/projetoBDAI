# Generated by Django 4.2.6 on 2025-01-03 04:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_playlistmusic_playlist_playlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlistmusic',
            name='playlist_playlist',
            field=models.ForeignKey(db_column='playlist_playlist_id', on_delete=django.db.models.deletion.PROTECT, to='app.playlist'),
        ),
    ]
