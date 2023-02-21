from django.urls import reverse
from django.db import models

# Create your models here.
class Categoria(models.Model):
    nombre_categoria = models.CharField( unique=True , max_length=50)
    slug = models.SlugField(max_length=100,unique=True)
    descripcion = models.TextField(max_length=255,blank=True)
    imagen_cat = models.ImageField(upload_to='photos/categoria')
    def __str__(self) -> str:
        return self.nombre_categoria
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def get_url(self):
            return reverse('productos_x_categoria', args=[self.slug])