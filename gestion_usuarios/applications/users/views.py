from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .functions import code_generator

from .forms import UserRegisterForm, LoginForm, UpdatePasswordForm,VerificationForm
from .models import User
# Create your views here.

#para crear superusuarios se utiliza el FormView ya que esta clase de usuarios es mas exigente
class UserRegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = '/'

    def form_valid(self,form):

        #generando codigo de verificacions
        codigo = code_generator()

        #creando usuario
        usuario = User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            nombres = form.cleaned_data['nombres'],
            apellidos = form.cleaned_data['apellidos'],
            genero = form.cleaned_data['genero'],
            coderegistro = codigo
        )
        # enviando el codigo email del user
        asunto = 'Confirmacion de email'
        mensaje = 'Codigo de verificacion:' + ' ' + codigo
        email_remitente = 'sebastian.cifuentes0808@gmail.com'

        #Recordar la configuracion del correo en el archivo settings
        send_mail(asunto, mensaje, email_remitente, [form.cleaned_data['email'],])
        #redirigir a pantalla dee validacion
        return HttpResponseRedirect(
            reverse(
                'users_app:user_verification',
                kwargs={'pk':usuario.id}
            )   
        )

#Iniciando sesion
class LoginUser(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home_app:panel')

    def form_valid(self,form):

        #autenticando el usuario
        user = authenticate(
            username = form.cleaned_data['username'],
            password = form.cleaned_data['password']
        )
        login (self.request, user)

        return super(LoginUser, self).form_valid(form)

#Cerrando sesion
class LogoutView(View):
    
    def get(self,request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(
            reverse(
                'users_app:user_login'
            )   
        )

#Actualizando la contrasenia
class UpdatePassword(LoginRequiredMixin, FormView):
    template_name = 'users/update_password.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('users_app:user_login')
    login_url = reverse_lazy('users_app:user_login')

    def form_valid(self,form):

        #Peticion para saber que usario esta activo en el momento de pedir el cambio de contrasenia
        usuario = self.request.user

        #Autenticando al usuario
        user = authenticate(
            username = usuario.username,
            password = form.cleaned_data['password']
        )
        
        #verificando la nueva contrasenia
        if user:
            new_password = form.cleaned_data['password_nueva']
            #la funcion .set_password la creamos en el managers.py de users
            usuario.set_password(new_password)
            usuario.save()

        logout(self.request)
        return super(UpdatePassword, self).form_valid(form)


class CodeVerificationView(FormView):
    template_name = 'users/verificacion.html'
    form_class = VerificationForm
    success_url = reverse_lazy('users_app:user_login')

    #Funcion para obtener los kwargs(parametros) y mandarselos al Form 
    def get_form_kwargs(self):
        kwargs = super(CodeVerificationView, self).get_form_kwargs()
        kwargs.update({
            'pk':self.kwargs['pk']
        })
        return kwargs


    def form_valid(self,form):

        User.objects.filter(
            id=self.kwargs["pk"]
        ).update(
            is_active = True
        )

        return super(CodeVerificationView, self).form_valid(form)
