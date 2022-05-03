from django import forms
from django.contrib.auth import authenticate

from .models import User

class UserRegisterForm(forms.ModelForm):

    #Aqui es donde se piden las contrasenias de forma mas segura
    password1 = forms.CharField(
        label = 'Contrasenia',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Constrasenia'
            }
        )
    )

    password2 = forms.CharField(
        label = 'Contrasenia',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Repetir Constrasenia'
            }
        )
    )

    class Meta:
        model = User
        #Jamas se guarda una contrasenia como dato plano, es por ello que no lo pedimos en los fields
        fields = (
            'username',
            'email',
            'nombres',
            'apellidos',
            'genero'
        )

    

    #validacion si la contrasenia 2 es diferente a la 1
    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2','Las contrasenias no son iguales')
        #Verificando que la contrasenia tenga mas de 5 caracteres    
        elif len(self.cleaned_data['password1']) < 5:
            self.add_error('password1','Las contrasenias deben tener mas de 5 digitos')   

#heredamos del Form normal ya que no dependemos de ningun modelo
class LoginForm(forms.Form):

    username = forms.CharField(
        label = 'username',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder':'Username'
            }
        )
    )

    password = forms.CharField(
        label = 'Contrasenia',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':' Constrasenia'
            }
        )
    )
        

    def clean(self):
        cleaner_data = super(LoginForm, self).clean
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not authenticate(username = username, password= password):
            raise forms.ValidationError('Los datos del usuario no son correctos')

        return self.cleaned_data

#actualizando la password
class UpdatePasswordForm(forms.Form):

    password = forms.CharField(
        label = 'Contrasenia',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':' Constrasenia Actual'
            }
        )
    )

    password_nueva = forms.CharField(
        label = 'Contrasenia Nueva',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':' Constrasenia Nueva'
            }
        )
    )

        
class VerificationForm(forms.Form):
    coderegistro = forms.CharField(required=True)

    #Recibiendo contexto de args y kwargs de la view CodeVerificationView
    def __init__(self, pk, *args, **kwargs):
        self.id_user = pk
        super(VerificationForm, self).__init__(*args, **kwargs)


    def clean_coderegistro(self):
        codigo = self.cleaned_data['coderegistro']

        if len(codigo) == 6:
            #Verificamos si el codigo y el id de usuario son validos
            #Para hacer esto, debemos de crear primero la validacion en managers.py
            activo = User.objects.cod_validation(
                self.id_user,
                codigo
            )
            if not activo:
                raise forms.ValidationError('El codigo es incorrecto')    
        else:
            raise forms.ValidationError('El codigo es incorrecto')

        
