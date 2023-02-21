from django.urls import path
from . import views
urlpatterns = [
    path('',views.tienda,name='tienda'),
    path('categoria/<slug:categoria_slug>/',views.tienda,name='productos_x_categoria'),
    path('categoria/<slug:categoria_slug>/<slug:producto_slug>/',views.detalleProducto,name='detalle_producto'),
    path('buscar/', views.buscar, name='buscar'),
    path('enviar_comentario/<int:producto_id>/', views.enviar_comentario, name='enviar_comentario'),
]
