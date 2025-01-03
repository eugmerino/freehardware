# Generated by Django 4.2.5 on 2024-11-23 23:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Nombre')),
                ('image', models.ImageField(upload_to='components/', verbose_name='imagen')),
            ],
            options={
                'verbose_name': 'Componente',
                'verbose_name_plural': 'Componentes',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Título')),
                ('description', models.TextField(max_length=400, verbose_name='Descripción')),
                ('state', models.IntegerField(choices=[(0, 'Inactivo'), (1, 'Activo'), (2, 'En revisión')], default=2, verbose_name='Estado')),
                ('imgDiagram', models.ImageField(upload_to='diagrams/', verbose_name='Diagrama')),
                ('code', models.TextField(verbose_name='Código fuente')),
                ('urlVideo', models.CharField(max_length=200, verbose_name='Video')),
                ('favorite', models.BooleanField(default=False, verbose_name='Destacado')),
            ],
            options={
                'verbose_name': 'Proyecto',
                'verbose_name_plural': 'Proyectos',
            },
        ),
        migrations.CreateModel(
            name='ProjectImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='projects/', verbose_name='imagen')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hardwareProject.project', verbose_name='Proyecto')),
            ],
            options={
                'verbose_name': 'Imagen',
                'verbose_name_plural': 'Imagenes',
            },
        ),
        migrations.CreateModel(
            name='ProjectComponent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(default=1, verbose_name='Cantidad')),
                ('description', models.TextField(blank=True, max_length=400, null=True, verbose_name='Descripción')),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_components', to='hardwareProject.component', verbose_name='Componente')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_components', to='hardwareProject.project', verbose_name='Proyecto')),
            ],
            options={
                'verbose_name': 'Proyecto-Componente',
                'verbose_name_plural': 'Proyectos-Componentes',
                'unique_together': {('project', 'component')},
            },
        ),
    ]
