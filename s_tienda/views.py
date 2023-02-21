from django.shortcuts import render,get_object_or_404,redirect

# Create your views here.
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from categoria.models import Categoria
from .models import Producto,Valoracion,GaleriaProducto
from carrito.models import CarroItem
from carrito.views import _carro_id

from .forms import ValoracionForm
from django.contrib import messages
from pedidos.models import PedidoProducto



def tienda(request, categoria_slug=None):
    categorias = None
    productos = None

    if categoria_slug != None:
        categorias = get_object_or_404(Categoria, slug=categoria_slug)
        productos = Producto.objects.filter(categoria=categorias, es_disponible=True)
        paginador = Paginator(productos, 1)
        pagina = request.GET.get('pagina')
        productos_paginados = paginador.get_page(pagina)
        contar_productos = productos.count()
    else:
        productos = Producto.objects.all().filter(es_disponible=True).order_by('id')
        
        paginador = Paginator(productos, 3)
        pagina = request.GET.get('pagina')
        productos_paginados = paginador.get_page(pagina)
        contar_productos = productos.count()

    context = {
        #'productos': productos, muestra sin paginacion abojo si
        'productos': productos_paginados,
        'contar_productos': contar_productos,
    }
    return render(request, 'tienda/tienda.html', context)


def detalleProducto(request, categoria_slug, producto_slug):
    try:
        producto_unico = Producto.objects.get(categoria__slug=categoria_slug, slug=producto_slug)
        en_carro = CarroItem.objects.filter(carro__carro_id=_carro_id(request), producto=producto_unico).exists()
    except Exception as e:
        raise e
        
    #valoracion
    if request.user.is_authenticated:
        try:
            pedidoproducto = PedidoProducto.objects.filter(user=request.user, producto_id=producto_unico.id).exists()
        except PedidoProducto.DoesNotExist:
            pedidoproducto = None
    else:
        pedidoproducto = None

    # Obtén las reseñas
    reseñas = Valoracion.objects.filter(producto_id=producto_unico.id, estado=True)

    # Obtener la galería de productos
    galeria_producto = GaleriaProducto.objects.filter(producto_id=producto_unico.id)

    context = {
        'producto_unico': producto_unico,
        'en_carro'       : en_carro,
        'pedidoproducto': pedidoproducto,
        'reseñas': reseñas,
        'galeria_producto': galeria_producto,
    }
    return render(request, 'tienda/detalle_producto.html', context)

def buscar(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            productos = Producto.objects.order_by('-fecha_creacion').filter(Q(descripcion__icontains=keyword) | Q(nombre_producto__icontains=keyword))
            contar_producto = productos.count()
                                                             
    context = {
        'productos': productos,
        'contar_productos': contar_producto,
    }
    return render(request, 'tienda/tienda.html', context)  

def enviar_comentario(request, producto_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reseña = Valoracion.objects.get(user__id=request.user.id, producto__id=producto_id)
            form = ValoracionForm(request.POST, instance=reseña)
            form.save()
            messages.success(request, 'Gracias. Su opinión ha sido actualizada.')
            return redirect(url)
        except Valoracion.DoesNotExist:
            form = ValoracionForm(request.POST)
            if form.is_valid():
                data = Valoracion()
                data.asunto = form.cleaned_data['asunto']
                data.valoracion = form.cleaned_data['valoracion']
                data.reseña = form.cleaned_data['reseña']
                data.ip = request.META.get('REMOTE_ADDR')
                data.producto_id = producto_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Gracias. Su opinión ha sido enviada.')
                return redirect(url)
                                               