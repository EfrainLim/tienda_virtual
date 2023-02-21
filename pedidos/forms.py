from django import forms
from .models import Pedido


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['nombres', 'apellidos', 'telefono', 'email', 'direccion_1',
         'direccion_2', 'pais', 'region', 'ciudad', 'nota_pedido'
         ]
      