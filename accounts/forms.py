from django import forms
from .models import Account, PerfilUsuario


class RegistracionForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Ingrese Password',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirme Password'
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def clean(self):
        cleaned_data = super(RegistracionForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "La contraseña no coincide."
            )

    def __init__(self, *args, **kwargs):
        super(RegistracionForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Ingrese Nombres'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Ingrese Apellidos'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Igrese número de celular'
        self.fields['email'].widget.attrs['placeholder'] = 'Ingrese correo electrónico'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number')

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class PerfilUsuarioForm(forms.ModelForm):
    foto_perfil = forms.ImageField(required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput)
    class Meta:
        model = PerfilUsuario
        fields = ('direccion_1', 'direccion_2', 'ciudad', 'estado', 'pais', 'foto_perfil')

    def __init__(self, *args, **kwargs):
        super(PerfilUsuarioForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
