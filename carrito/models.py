from django.db import models
from s_tienda.models import Producto , Variacion
from accounts.models import Account


# Create your models here.

class Carro(models.Model):
    carro_id = models.CharField(max_length=250, blank=True)
    fecha_agregada = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.carro_id


class CarroItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    variaciones = models.ManyToManyField(Variacion, blank=True)
    carro    = models.ForeignKey(Carro, on_delete=models.CASCADE, null=True)
    cantidad = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.producto.precio * self.cantidad

    def __unicode__(self):
        return self.producto
    