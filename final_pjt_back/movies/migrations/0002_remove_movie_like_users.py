# Generated by Django 3.2.3 on 2021-05-21 02:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='like_users',
        ),
    ]
