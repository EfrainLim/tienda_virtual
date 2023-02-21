from django.urls import path
from . import views


urlpatterns = [
    path('registrar/', views.registrar, name='registrar'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('cuenta/', views.cuenta, name='cuenta'),
    # path('', views.dashboard, name='dashboard'),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),

    #para ver en pelfil
    path('mis_pedidos/', views.mis_pedidos, name='mis_pedidos'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('cambiar_pasword/', views.cambiar_pasword, name='cambiar_pasword'),
    path('detalle_pedido/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),


]
