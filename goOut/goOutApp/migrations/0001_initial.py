# Generated by Django 5.0.1 on 2024-03-03 22:07

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaComida',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('imagen', models.ImageField(upload_to='imagen_categoria_comida')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Emprendedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('edad', models.IntegerField()),
                ('nombre', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Contacto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField()),
                ('direccion', models.CharField(max_length=255)),
                ('direccion_secundaria', models.CharField(blank=True, max_length=255, null=True)),
                ('correo', models.EmailField(max_length=254)),
                ('telefono', models.CharField(max_length=20)),
                ('latitud', models.FloatField(blank=True, null=True)),
                ('longitud', models.FloatField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('emprendedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goOutApp.emprendedor')),
            ],
        ),
        migrations.CreateModel(
            name='Comida',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('descripcion', models.CharField(max_length=100)),
                ('imagen', models.ImageField(upload_to='imagen_comida')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('categoriaComida', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goOutApp.categoriacomida')),
                ('emprendedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goOutApp.emprendedor')),
            ],
        ),
        migrations.CreateModel(
            name='CategoriaEvento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('imagen', models.ImageField(upload_to='imagen_categoria_evento')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('emprendedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goOutApp.emprendedor')),
            ],
        ),
        migrations.AddField(
            model_name='categoriacomida',
            name='emprendedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goOutApp.emprendedor'),
        ),
        migrations.CreateModel(
            name='Emprendimiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('emprendedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goOutApp.emprendedor')),
            ],
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=100)),
                ('disponibles', models.IntegerField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('categoriaEvento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goOutApp.categoriaevento')),
                ('emprendedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goOutApp.emprendedor')),
            ],
        ),
        migrations.CreateModel(
            name='Galeria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('emprendedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goOutApp.emprendedor')),
                ('eventos', models.ManyToManyField(to='goOutApp.evento')),
            ],
        ),
        migrations.CreateModel(
            name='ImagenContacto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to='imagen_contacto')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('contacto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagenesContacto', to='goOutApp.contacto')),
            ],
        ),
        migrations.CreateModel(
            name='ImagenEvento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to='imagen_evento')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagenesEvento', to='goOutApp.evento')),
            ],
        ),
        migrations.CreateModel(
            name='SobreNos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('emprendedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goOutApp.emprendedor')),
            ],
        ),
        migrations.CreateModel(
            name='ImagenSobreNos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to='imagen_sobre_nos')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('sobreNos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagenesSobreNos', to='goOutApp.sobrenos')),
            ],
        ),
    ]
