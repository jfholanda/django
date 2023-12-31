# Generated by Django 4.2.4 on 2023-12-05 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avaliacoes', '0002_avaliacao_delete_avaliacoes'),
        ('comentarios', '0001_initial'),
        ('core', '0003_pontoturistico_comentario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pontoturistico',
            name='comentario',
        ),
        migrations.AddField(
            model_name='pontoturistico',
            name='avaliacoes',
            field=models.ManyToManyField(to='avaliacoes.avaliacao'),
        ),
        migrations.AddField(
            model_name='pontoturistico',
            name='comentarios',
            field=models.ManyToManyField(to='comentarios.comentario'),
        ),
    ]
