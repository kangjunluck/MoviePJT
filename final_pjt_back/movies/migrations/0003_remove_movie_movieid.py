# Generated by Django 3.2.3 on 2021-05-21 02:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_remove_movie_like_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='movieid',
        ),
    ]
