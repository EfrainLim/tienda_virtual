# Generated by Django 4.1.4 on 2022-12-19 21:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categoria', '0002_alter_categoria_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_producto', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('descripcion', models.TextField(blank=True, max_length=500)),
                ('precio', models.IntegerField()),
                ('imagenes', models.ImageField(upload_to='photos/productos')),
                ('stock', models.IntegerField()),
                ('es_disponible', models.BooleanField(default=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categoria.categoria')),
            ],
        ),
    ]