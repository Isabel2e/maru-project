# Generated by Django 5.1.3 on 2024-12-06 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comentario', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=100, verbose_name='Palabra')),
                ('language', models.CharField(max_length=10, verbose_name='Idioma')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
            ],
        ),
    ]
