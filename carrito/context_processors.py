from .models import Carro, CarroItem
from .views import _carro_id


def contador(request):
    contar_carro = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            carro = Carro.objects.filter(carro_id=_carro_id(request))
            if request.user.is_authenticated:
                carro_items = CarroItem.objects.all().filter(user=request.user)
            else:
                carro_items = CarroItem.objects.all().filter(carro=carro[:1])
            for carro_item in carro_items:
                contar_carro += carro_item.cantidad
        except Carro.DoesNotExist:
            contar_carro = 0
    return dict(contar_carro=contar_carro)
