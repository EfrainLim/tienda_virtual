from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from carrito.models import CarroItem
from .forms import PedidoForm
import datetime
from .models import Pedido, Pago, PedidoProducto
import json
from  s_tienda.models import Producto
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def pagos(request):
    body = json.loads(request.body)
    pedido = Pedido.objects.get(user=request.user, esta_ordenado=False, numero_pedido=body['pedidoID'])    
    # Almacenar los datos de la transacción en el modelo de pago
    pago = Pago(
        user = request.user,
        pago_id = body['transID'],
        metodo_pago = body['metodo_pago'],
        importe_pagado = pedido.total_pedido,
        estado = body['estado'],
    )
    pago.save()

    pedido.pago = pago
    pedido.esta_ordenado = True
    pedido.save()

    # Mover los artículos del carrito a la tabla de Pedido producto
    carro_items = CarroItem.objects.filter(user=request.user)

    for item in carro_items:
        pedidoproducto = PedidoProducto()
        pedidoproducto.pedido_id = pedido.id
        pedidoproducto.pago = pago
        pedidoproducto.user_id = request.user.id
        pedidoproducto.producto_id = item.producto_id
        pedidoproducto.cantidad = item.cantidad
        pedidoproducto.precio_producto = item.producto.precio
        pedidoproducto.ordenado = True
        pedidoproducto.save()

        carro_item = CarroItem.objects.get(id=item.id)
        producto_variacion = carro_item.variaciones.all()
        pedidoproducto = PedidoProducto.objects.get(id=pedidoproducto.id)
        pedidoproducto.variaciones.set(producto_variacion)
        pedidoproducto.save()

        # Reduce the quantity of the sold products
        producto = Producto.objects.get(id=item.producto_id)
        producto.stock -= item.cantidad
        producto.save()

    # Eliminar Carrito
    CarroItem.objects.filter(user=request.user).delete()

    # Enviar email de pedido recibido al cliente
    mail_subject = 'Gracias por su pedido.'
    message = render_to_string('pedidos/correo_recibido_pedido.html', {
        'user': request.user,
        'pedido': pedido,
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

    # Enviar número de pedido e id de transacción de vuelta al método sendData vía JsonResponse
    
    data = {
        'numero_pedido': pedido.numero_pedido,
        'transID': pago.pago_id,
    }
    print(data)
    return JsonResponse(data)


def realizar_pedido(request, total=0, cantidad=0,):
    usuario_actual = request.user

    # If the cart count is less than or equal to 0, then redirect back to shop
    carro_items = CarroItem.objects.filter(user=usuario_actual)
    carro_count = carro_items.count()
    if carro_count <= 0:
        return redirect('tienda')

    total_general = 0
    tax = 0
    for carro_item in carro_items:
        total += (carro_item.producto.precio * carro_item.cantidad)
        cantidad += carro_item.cantidad
    tax = (2 * total)/100
    total_general = total + tax

    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            # Store all the billing information inside Order table
            data = Pedido()
            data.user = usuario_actual
            data.nombres = form.cleaned_data['nombres']
            data.apellidos = form.cleaned_data['apellidos']
            data.telefono = form.cleaned_data['telefono']
            data.email = form.cleaned_data['email']
            data.direccion_1 = form.cleaned_data['direccion_1']
            data.direccion_2 = form.cleaned_data['direccion_2']
            data.pais = form.cleaned_data['pais']
            data.region = form.cleaned_data['region']
            data.ciudad = form.cleaned_data['ciudad']
            data.nota_pedido = form.cleaned_data['nota_pedido']
            data.total_pedido = total_general
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            fecha_actual = d.strftime("%Y%m%d") #20210305
            numero_pedido = fecha_actual + str(data.id)
            data.numero_pedido = numero_pedido
            data.save()

            pedido = Pedido.objects.get(user=usuario_actual, esta_ordenado=False, numero_pedido=numero_pedido)
            context = {
                'pedido': pedido,
                'carro_items': carro_items,
                'total': total,
                'tax': tax,
                'total_general': total_general,
            }
            return render(request, 'pedidos/pagos.html', context)
    else:
        return redirect('checkout')


def pedido_completado(request):
    numero_pedido = request.GET.get('numero_pedido')
    transID = request.GET.get('pago_id')
    try:
        pedido = Pedido.objects.get(numero_pedido=numero_pedido, esta_ordenado=True)
        productos_pedidos = PedidoProducto.objects.filter(pedido_id=pedido.id)

        subtotal = 0
        for i in productos_pedidos:
            subtotal += i.precio_producto * i.cantidad

        pago = Pago.objects.get(pago_id=transID)

        context = {
            'pedido': pedido,
            'productos_pedidos': productos_pedidos,
            'numero_pedido': pedido.numero_pedido,
            'transID': pago.pago_id,
            'pago': pago,
            'subtotal': subtotal,
        }
        return render(request, 'pedidos/pedido_completado.html', context)
    except (Pago.DoesNotExist, Pedido.DoesNotExist):
        return redirect('inicio')
