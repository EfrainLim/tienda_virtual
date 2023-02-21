from django.shortcuts import render

from s_tienda.models import Producto,Valoracion
def principal(request):
    productos=Producto.objects.all().filter(es_disponible=True).order_by('fecha_creacion')
    reseñas = None
    for producto in productos:
        reseñas = Valoracion.objects.filter(producto_id=producto.id, estado=True)
    context={
        'productos':productos,
        'reseñas': reseñas,
    }
    return render(request, 'index.html',context)