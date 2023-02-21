from django.contrib import admin
from .models import Producto,Variacion,Valoracion,GaleriaProducto
import admin_thumbnails

@admin_thumbnails.thumbnail('imagen')
class GaleriaProductoInline(admin.TabularInline):
    model = GaleriaProducto
    extra = 1

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre_producto', 'precio', 'stock', 'categoria', 'fecha_modificacion', 'es_disponible')
    prepopulated_fields = {'slug': ('nombre_producto',)}
    inlines = [GaleriaProductoInline]

class VariacionAdmin(admin.ModelAdmin):
    list_display = ('producto', 'variacion_categoria', 'variacion_valor', 'es_activo')
    list_editable = ('es_activo',)
    list_filter = ('producto', 'variacion_categoria', 'variacion_valor')

admin.site.register(Producto,ProductoAdmin)
admin.site.register(Variacion,VariacionAdmin)
admin.site.register(Valoracion)
admin.site.register(GaleriaProducto)
