from django.urls import path
from . import views
urlpatterns = [
    path('',views.carrito,name='carrito'),
    path('agregar_carro/<int:producto_id>/', views.agregar_carro, name='agregar_carro'),
    path('eliminar_carro/<int:producto_id>/<int:carro_item_id>/', views.eliminar_carro, name='eliminar_carro'),
    path('eliminar_item_carro/<int:producto_id>/<int:carro_item_id>/', views.quitar_item_carro, name='eliminar_item_carro'),
    
    path('checkout/', views.checkout, name='checkout'),
]
