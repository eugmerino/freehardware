# Generated by Django 4.2.5 on 2024-11-23 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SystemConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Nombre')),
                ('acronym', models.CharField(max_length=10, verbose_name='Acrónimo')),
                ('logo', models.ImageField(upload_to='logo/', verbose_name='Logo')),
            ],
            options={
                'verbose_name': 'Configuración del sistema',
                'verbose_name_plural': 'Configuración del sistema',
            },
        ),
    ]
