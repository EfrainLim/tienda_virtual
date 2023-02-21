from django.urls import path
from . import views

urlpatterns = [
    path('realizar_pedido/', views.realizar_pedido, name='realizar_pedido'),
    path('pagos/', views.pagos, name='pagos'),
    path('pedido_completado/', views.pedido_completado, name='pedido_completado'),
]
