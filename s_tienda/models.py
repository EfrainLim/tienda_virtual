
from django.db import models
from categoria.models import Categoria
from django.urls import reverse
from accounts.models import Account
from django.db.models import Avg, Count

# Create your models here.

class Producto(models.Model):
    nombre_producto    = models.CharField(max_length=200, unique=True)
    slug            = models.SlugField(max_length=200, unique=True)
    descripcion     = models.TextField(max_length=500, blank=True)
    precio           = models.IntegerField()
    imagenes          = models.ImageField(upload_to='photos/productos')
    stock           = models.IntegerField()
    es_disponible    = models.BooleanField(default=True)
    categoria        = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    fecha_creacion    = models.DateTimeField(auto_now_add=True)
    fecha_modificacion   = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('detalle_producto', args=[self.categoria.slug, self.slug])

    def __str__(self):
        return self.nombre_producto

    #calcula el promedio de valoraciones de 1 a 5
    def revisionMedia(self):
        reseñas = Valoracion.objects.filter(producto=self, estado=True).aggregate(promedio=Avg('valoracion'))
        pmd = 0
        if reseñas['promedio'] is not None:
            pmd = float(reseñas['promedio'])
        return pmd
    #cuenta cuantas personas calificaron
    def contarReseñas(self):
        reseñas = Valoracion.objects.filter(producto=self, estado=True).aggregate(contar=Count('id'))
        contar = 0
        if reseñas['contar'] is not None:
            contar = int(reseñas['contar'])
        return contar


class VariacionManager(models.Manager):
    def colores(self):
        return super(VariacionManager, self).filter(variacion_categoria='color', es_activo=True)

    def tamaños(self):
        return super(VariacionManager, self).filter(variacion_categoria='tamaño', es_activo=True)

eleccion_categoria_variacion = (
    ('color', 'color'),
    ('tamaño', 'tamaño'),
)

class Variacion(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    variacion_categoria = models.CharField(max_length=100, choices=eleccion_categoria_variacion)
    variacion_valor     = models.CharField(max_length=100)
    es_activo           = models.BooleanField(default=True)
    fecha_creacion        = models.DateTimeField(auto_now=True)

    objects = VariacionManager()

    def __str__(self):
        return self.variacion_valor


class Valoracion(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    asunto = models.CharField(max_length=100, blank=True)
    reseña = models.TextField(max_length=500, blank=True)
    valoracion = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    estado = models.BooleanField(default=True)
    fecha_de_creación = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.asunto

class GaleriaProducto(models.Model):
    producto = models.ForeignKey(Producto, default=None, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='tienda/productos', max_length=255)

    def __str__(self):
        return self.producto.nombre_producto

    class Meta:
        verbose_name = 'Galeria Foto'
        verbose_name_plural = 'Galeria Fotos'
