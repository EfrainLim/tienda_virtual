from django.contrib import admin
from .models import Pago, Pedido, PedidoProducto
# Register your models here.


class PedidoProductInline(admin.TabularInline):
    model = PedidoProducto
    readonly_fields = ('pago', 'user', 'producto', 'cantidad', 'precio_producto', 'ordenado')
    extra = 0

class PedidoAdmin(admin.ModelAdmin):
    list_display = ['numero_pedido', 'nombre_completo', 'telefono', 'email', 'ciudad', 'total_pedido', 'tax', 'estado', 'esta_ordenado', 'fecha_de_creacion']
    list_filter = ['estado', 'esta_ordenado']
    search_fields = ['numero_pedido', 'nombres', 'apellidos', 'telefono', 'email']
    list_per_page = 20
    inlines = [PedidoProductInline]

admin.site.register(Pago)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(PedidoProducto)

