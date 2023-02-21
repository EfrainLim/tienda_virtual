from django.db import models
from accounts.models import Account
from s_tienda.models import Producto, Variacion
# Create your models here.
class Pago(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    pago_id = models.CharField(max_length=100)
    metodo_pago = models.CharField(max_length=100)
    importe_pagado = models.CharField(max_length=100) # this is the total amount paid
    estado = models.CharField(max_length=100)
    fecha_de_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pago_id

class Pedido(models.Model):
    STATUS = (
        ('Nuevo', 'Nuevo'),
        ('Aceptado', 'Aceptado'),
        ('Completado', 'Completado'),
        ('Cancelado', 'Cancelled'),
    )

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    pago = models.ForeignKey(Pago, on_delete=models.SET_NULL, blank=True, null=True)
    numero_pedido = models.CharField(max_length=20)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    direccion_1 = models.CharField(max_length=50)
    direccion_2 = models.CharField(max_length=50, blank=True)
    pais = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=50)
    nota_pedido = models.CharField(max_length=100, blank=True)
    total_pedido = models.FloatField()
    tax = models.FloatField()
    estado = models.CharField(max_length=10, choices=STATUS, default='Nuevo')
    ip = models.CharField(blank=True, max_length=20)
    esta_ordenado = models.BooleanField(default=False)
    fecha_de_creacion = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)


    def nombre_completo(self):
        return f'{self.nombres} {self.apellidos}'

    def direccion_completa(self):
        return f'{self.direccion_1} {self.direccion_2}'

    def __str__(self):
        return self.nombres


class PedidoProducto(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    pago = models.ForeignKey(Pago, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    variaciones = models.ManyToManyField(Variacion, blank=True)
    cantidad = models.IntegerField()
    precio_producto = models.FloatField()
    ordenado = models.BooleanField(default=False)
    fecha_de_creacion = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.producto.nombre_producto

