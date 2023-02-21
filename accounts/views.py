from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistracionForm , UsuarioForm, PerfilUsuarioForm
from .models import Account, PerfilUsuario
from pedidos.models import Pedido, PedidoProducto
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from carrito.views import _carro_id
from carrito.models import Carro, CarroItem
import requests


def registrar(request):
    if request.method == 'POST':
        form = RegistracionForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()

            # Create a user profile
            perfil = PerfilUsuario()
            perfil.user_id = user.id
            perfil.foto_perfil = 'default/default-user.png'
            perfil.save()

            # USER ACTIVATION
            sitio_actual = get_current_site(request)
            mail_subject = 'Por favor, active su cuenta'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': sitio_actual,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            # messages.success(request, 'Thank you for registering with us. We have sent you a verification email to your email address [rathan.kumar@gmail.com]. Please verify it.')
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form = RegistracionForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/registrar.html', context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                carro = Carro.objects.get(carro_id=_carro_id(request))
                is_cart_item_exists = CarroItem.objects.filter(carro=carro).exists()
                if is_cart_item_exists:
                    carro_item = CarroItem.objects.filter(carro=carro)

                    # Getting the product variations by cart id
                    producto_variacion = []
                    for item in carro_item:
                        variation = item.variaciones.all()
                        producto_variacion.append(list(variation))

                    # Get the cart items from the user to access his product variations
                    carro_item = CarroItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in carro_item:
                        existing_variation = item.variaciones.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    # product_variation = [1, 2, 3, 4, 6]
                    # ex_var_list = [4, 6, 3, 5]

                    for pr in producto_variacion:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CarroItem.objects.get(id=item_id)
                            item.cantidad += 1
                            item.user = user
                            item.save()
                        else:
                            carro_item = CarroItem.objects.filter(carro=carro)
                            for item in carro_item:
                                item.user = user
                                item.save()
            except:
                pass
            auth.login(request, user)
            messages.success(request, 'Ha iniciado sesión.')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                # next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('cuenta')
        else:
            messages.error(request, 'Credenciales de inicio de sesión no válidas')
            return redirect('login')
    return render(request, 'accounts/login.html')


@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'Ha cerrado la sesión.')
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Enhorabuena. Su cuenta está activada.')
        return redirect('login')
    else:
        messages.error(request, 'Enlace de activación inválido')
        return redirect('registrar')


@login_required(login_url = 'login')
def cuenta(request):
    pedidos = Pedido.objects.order_by('-fecha_de_creacion').filter(user_id=request.user.id, esta_ordenado=True)
    numero_pedidos = pedidos.count()

    perfilusuario = PerfilUsuario.objects.get(user_id=request.user.id)
    context = {
        'numero_pedidos': numero_pedidos,
        'perfilusuario': perfilusuario,
    }
    return render(request, 'accounts/cuenta.html', context)


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Correo electrónico de restablecimiento de contraseña
            sitio_actual = get_current_site(request)
            mail_subject = 'Restablecer contraseña'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': sitio_actual,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Se ha enviado un correo electrónico de restablecimiento de contraseña a su correo electrónico.')
            return redirect('login')
        else:
            messages.error(request, 'La cuenta no existe.')
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Restablecer contraseña')
        return redirect('resetPassword')
    else:
        messages.error(request, 'Este enlace ha caducado!.')
        return redirect('login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')


@login_required(login_url='login')
def mis_pedidos(request):
    pedidos = Pedido.objects.filter(user=request.user, esta_ordenado=True).order_by('-fecha_de_creacion')
    context = {
        'pedidos': pedidos,
    }
    return render(request, 'accounts/mis_pedidos.html', context)


@login_required(login_url='login')
def editar_perfil(request):
    perfilusuario = get_object_or_404(PerfilUsuario, user=request.user)
    if request.method == 'POST':
        usuario_form = UsuarioForm(request.POST, instance=request.user)
        perfil_form = PerfilUsuarioForm(request.POST, request.FILES, instance=perfilusuario)
        if usuario_form.is_valid() and perfil_form.is_valid():
            usuario_form.save()
            perfil_form.save()
            messages.success(request, 'Su perfil ha sido actualizado.')
            return redirect('editar_perfil')
    else:
        usuario_form = UsuarioForm(instance=request.user)
        perfil_form = PerfilUsuarioForm(instance=perfilusuario)
    context = {
        'usuario_form': usuario_form,
        'perfil_form': perfil_form,
        'perfilusuario': perfilusuario,
    }
    return render(request, 'accounts/editar_perfil.html', context)


@login_required(login_url='login')
def cambiar_pasword(request):
    if request.method == 'POST':
        contraseña_actual = request.POST['contraseña_actual']
        nueva_contraseña = request.POST['nueva_contraseña']
        confirmar_contraseña = request.POST['confirmar_contraseña']

        user = Account.objects.get(username__exact=request.user.username)

        if nueva_contraseña == confirmar_contraseña:
            success = user.check_password(contraseña_actual)
            if success:
                user.set_password(nueva_contraseña)
                user.save()
                # auth.logout(request)
                messages.success(request, 'Contraseña actualizada correctamente.')
                return redirect('cambiar_pasword')
            else:
                messages.error(request, 'Introduzca una contraseña válida')
                return redirect('cambiar_pasword')
        else:
            messages.error(request, 'La contraseña no coincide.')
            return redirect('cambiar_pasword')
    return render(request, 'accounts/cambiar_pasword.html')


@login_required(login_url='login')
def detalle_pedido(request, pedido_id):
    detalle_pedido = PedidoProducto.objects.filter(pedido__numero_pedido=pedido_id)
    pedido = Pedido.objects.get(numero_pedido=pedido_id)
    subtotal = 0
    for i in detalle_pedido:
        subtotal += i.precio_producto * i.cantidad

    context = {
        'detalle_pedido': detalle_pedido,
        'pedido': pedido,
        'subtotal': subtotal,
    }
    return render(request, 'accounts/detalle_pedido.html', context)
