from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
# Create your views here.

#El loginRequiredMixin es una libreria que obliga a un usuario a esta logeado en la pagina para acceder
# al apartado que el quiere.
class HomePage(LoginRequiredMixin, TemplateView):
    template_name = 'home/index.html'

    #Si el usuario no esta registrado e intenta logear, lo mandaremos a la url:
    login_url = reverse_lazy('users_app:user_login')