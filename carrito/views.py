from django.shortcuts import render, redirect, get_object_or_404
from s_tienda.models import Producto , Variacion
from .models import Carro, CarroItem

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.http import HttpResponse

def _carro_id(request):
    carro = request.session.session_key
    if not carro:
        carro = request.session.create()
    return carro

def agregar_carro(request, producto_id):
    usuario_actual = request.user
    print(usuario_actual)
    producto = Producto.objects.get(id=producto_id) #obtener el producto
    # Si el usuario está autenticado
    if usuario_actual.is_authenticated:
        producto_variacion = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                valor = request.POST[key]
                try:
                    variacion = Variacion.objects.get(producto=producto, variacion_categoria__iexact=key, variacion_valor__iexact=valor)
                    producto_variacion.append(variacion)
                except:
                    pass


        hay_articulo_en_carrito = CarroItem.objects.filter(producto=producto, user=usuario_actual).exists()
        if hay_articulo_en_carrito:
            carro_item = CarroItem.objects.filter(producto=producto, user=usuario_actual)
            ex_var_list = []
            id = []
            for item in carro_item:
                variacion_existente = item.variaciones.all()
                ex_var_list.append(list(variacion_existente))
                id.append(item.id)

            if producto_variacion in ex_var_list:
                # aumentar la cantidad de artículos de la cesta
                index = ex_var_list.index(producto_variacion)
                item_id = id[index]
                item = CarroItem.objects.get(producto=producto, id=item_id)
                item.cantidad += 1
                item.save()

            else:
                item = CarroItem.objects.create(producto=producto, cantidad=1, user=usuario_actual)
                if len(producto_variacion) > 0:
                    item.variaciones.clear()
                    item.variaciones.add(*producto_variacion)
                item.save()
        else:
            carro_item = CarroItem.objects.create(
                producto = producto,
                cantidad = 1,
                user = usuario_actual,
            )
            if len(producto_variacion) > 0:
                carro_item.variaciones.clear()
                carro_item.variaciones.add(*producto_variacion)
            carro_item.save()
        return redirect('carrito')
        
    # Si el usuario no está autenticado
    else:
        producto_variacion = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                valor = request.POST[key]

                try:
                    variacion = Variacion.objects.get(producto=producto, variacion_categoria__iexact=key, variacion_valor__iexact=valor)
                    producto_variacion.append(variacion)
                except:
                    pass

        try:
            carro = Carro.objects.get(carro_id=_carro_id(request)) # get the cart using the cart_id present in the session
        except Carro.DoesNotExist:
            carro = Carro.objects.create(
                carro_id = _carro_id(request)
            )
        carro.save()

        carro_item_existe = CarroItem.objects.filter(producto=producto, carro=carro).exists()
        if carro_item_existe:
            carro_item = CarroItem.objects.filter(producto=producto, carro=carro)
            #variaciones_existentes -> base_de_datos
            #variación actual -> variación_producto
            #item_id -> base de datos
            ex_var_list = []
            id = []
            for item in carro_item:
                variacion_existente = item.variaciones.all()
                ex_var_list.append(list(variacion_existente))
                id.append(item.id)

            print(ex_var_list)

            if producto_variacion in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(producto_variacion)
                item_id = id[index]
                item = CarroItem.objects.get(producto=producto, id=item_id)
                item.cantidad += 1
                item.save()

            else:
                item = CarroItem.objects.create(producto=producto, cantidad=1, carro=carro)
                if len(producto_variacion) > 0:
                    item.variaciones.clear()
                    item.variaciones.add(*producto_variacion)
                item.save()
        else:
            carro_item = CarroItem.objects.create(
                producto = producto,
                cantidad = 1,
                carro = carro,
            )
            if len(producto_variacion) > 0:
                carro_item.variaciones.clear()
                carro_item.variaciones.add(*producto_variacion)
            carro_item.save()
        return redirect('carrito')
    




def eliminar_carro(request, producto_id, carro_item_id):

    producto = get_object_or_404(Producto, id=producto_id)
    try:
        if request.user.is_authenticated:
            carro_item = CarroItem.objects.get(producto=producto, user=request.user, id=carro_item_id)
        else:
            carro = Carro.objects.get(carro_id=_carro_id(request))
            carro_item = CarroItem.objects.get(producto=producto, carro=carro, id=carro_item_id)
        if carro_item.cantidad > 1:
            carro_item.cantidad -= 1
            carro_item.save()
        else:
            carro_item.delete()
    except:
        pass
    return redirect('carrito')



def quitar_item_carro(request, producto_id, carro_item_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.user.is_authenticated:
        carro_item = CarroItem.objects.get(producto=producto, user=request.user, id=carro_item_id)
    else:
        carro = Carro.objects.get(carro_id=_carro_id(request))
        carro_item = CarroItem.objects.get(producto=producto, carro=carro, id=carro_item_id)
    carro_item.delete()
    return redirect('carrito')




def carrito(request, total=0, cantidad=0, carro_items=None):
    try:
        tax = 0
        total_general = 0
        if request.user.is_authenticated:
            carro_items = CarroItem.objects.filter(user=request.user, is_active=True)
        else:
            carro = Carro.objects.get(carro_id=_carro_id(request))
            carro_items = CarroItem.objects.filter(carro=carro, is_active=True)
        for carro_item in carro_items:
            total += (carro_item.producto.precio * carro_item.cantidad)
            cantidad += carro_item.cantidad
        tax = (2 * total)/100
        total_general = total + tax
    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        'total': total,
        'cantidad': cantidad,
        'carro_items': carro_items,
        'tax'       : tax,
        'total_general': total_general,
    }
    return render(request, 'tienda/carrito.html',context)


@login_required(login_url='login')
def checkout(request, total=0, cantidad=0, carro_items=None):
    try:
        tax = 0
        total_general = 0
        if request.user.is_authenticated:
            carro_items = CarroItem.objects.filter(user=request.user, is_active=True)
        else:
            carro = Carro.objects.get(carro_id=_carro_id(request))
            carro_items = CarroItem.objects.filter(carro=carro, is_active=True)
        for carro_item in carro_items:
            total += (carro_item.producto.precio * carro_item.cantidad)
            cantidad += carro_item.cantidad
        tax = (2 * total)/100
        total_general = total + tax
    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        'total': total,
        'cantidad': cantidad,
        'carro_items': carro_items,
        'tax'       : tax,
        'total_general': total_general,
    }
    return render(request, 'tienda/checkout.html', context)