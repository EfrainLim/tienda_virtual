from django.contrib import admin

from .models import Carro,CarroItem

# Register your models here.

class CarroAdmin(admin.ModelAdmin):
    list_display = ('carro_id', 'fecha_agregada')
class CarroItemAdmin(admin.ModelAdmin):
    list_display = ('producto', 'carro', 'cantidad', 'is_active')

admin.site.register(Carro,CarroAdmin)
admin.site.register(CarroItem,CarroItemAdmin)