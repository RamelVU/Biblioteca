import json
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.core.serializers import serialize
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, TemplateView
from .forms import FormularioLogin, UsuarioForm
from .models import Usuario
from .mixins import LoginYSuperStaffMixin, ValidarPermisosMixin

# Create your views here.

class Inicio(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

class Login(FormView):
    template_name = 'login.html'
    form_class = FormularioLogin
    success_url = reverse_lazy('index')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(Login, self).form_valid(form)

def logoutUsuario(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login/')

''' Clase para listar los usuarios antes de rabajar con Ajax
class ListadoUsuario(ListView):
    model = Usuario
    template_name = 'usuarios/listar_usuarios.html'
    queryset = Usuario.objects.filter(usuario_activo=True)
    context_object_name = 'usuarios'
'''

''' Clase para pintar la pagina de inicio antes de ponerla directamente en la url
class InicioListadoUsuario(TemplateView):
    template_name = 'usuarios/listar_usuarios.html' '''

class InicioUsuario(LoginYSuperStaffMixin, ValidarPermisosMixin, TemplateView):
    template_name = 'usuarios/listar_usuarios.html'
    permission_required = ('usuario.view_usuario', 'usuario.add_usuario', 'usuario.change_usuario', 'usuario.delete_usuario')

class ListadoUsuario(LoginYSuperStaffMixin, ValidarPermisosMixin, ListView):
    model = Usuario
    permission_required = ('usuario.view_usuario', 'usuario.add_usuario', 'usuario.change_usuario', 'usuario.delete_usuario')
    
    def get_queryset(self):
        return self.model.objects.filter(is_active=True)
    
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            ''' Manera de crear un json manual
                lista_usuarios = []
                for usuario in self.get_queryset():
                    data_usuario = {}
                    data_usuario['id'] = usuario.id
                    data_usuario['nombres'] = usuario.nombres
                    data_usuario['apellidos'] = usuario.apellidos
                    data_usuario['email'] = usuario.email
                    data_usuario['username'] = usuario.username
                    data_usuario['isactive'] = usuario.usuario_activo
                    lista_usuarios.append(data_usuario) 
                data = json.dumps(lista_usuarios)
                return HttpResponse(data, 'application/json')
            '''

            ''' Creando el json con serializer '''
            data = serialize('json', self.get_queryset())
            return HttpResponse(data, 'application/json')

        return redirect('usuario:inicio_usuarios')

'''Forma de crear usuarios sin ajax
class RegistrarUsuario(CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'usuarios/crear_usuario.html'
    # success_url = reverse_lazy('usuario:listar_usuarios')

    def post(self, request, *arg, **kwargs):
        form = self.form_class(request.POST) #obtengo toa la info del formulario una vez que lo manden
        if form.is_valid():
            nuevo_usuario = Usuario(
                email = form.cleaned_data['email'],
                username = form.cleaned_data['username'],
                nombres = form.cleaned_data['nombres'],
                apellidos = form.cleaned_data['apellidos'],
            )
            nuevo_usuario.set_password(form.cleaned_data['password1'])
            nuevo_usuario.save()
            return redirect('usuario:listar_usuarios')
        else:
            return render(request, self.template_name, {'form':form})
'''

class RegistrarUsuario(LoginYSuperStaffMixin, ValidarPermisosMixin, CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'usuarios/crear_usuario.html'
    permission_required = ('usuario.view_usuario', 'usuario.add_usuario', 'usuario.change_usuario', 'usuario.delete_usuario')
    # success_url = reverse_lazy('usuario:listar_usuarios')

    def post(self, request, *arg, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST) #obtengo toda la info del formulario una vez que lo manden
            if form.is_valid():
                nuevo_usuario = Usuario(
                    email = form.cleaned_data['email'],
                    username = form.cleaned_data['username'],
                    nombres = form.cleaned_data['nombres'],
                    apellidos = form.cleaned_data['apellidos'],
                )
                nuevo_usuario.set_password(form.cleaned_data['password1'])
                nuevo_usuario.save()
                mensaje = f'{self.model.__name__} registrado correctamente!'
                error = 'No hay error!'
                response = JsonResponse({'mensaje':mensaje, 'error':error})
                response.status_code = 201
                return response
            else:
                mensaje = f'{self.model.__name__} no se ha podido registrar!'
                error = form.errors
                response = JsonResponse({'mensaje':mensaje, 'error':error})
                response.status_code = 400
                return response
        else:
            return redirect('usuario:inicio_usuarios')

class EditarUsuario(LoginYSuperStaffMixin, ValidarPermisosMixin, UpdateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'usuarios/editar_usuario.html'
    permission_required = ('usuario.view_usuario', 'usuario.add_usuario', 'usuario.change_usuario', 'usuario.delete_usuario')

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST, instance=self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'{self.model.__name__} actualizado correctamente!'
                error = 'No hay error!'
                response = JsonResponse({'mensaje':mensaje, 'error':error})
                response.status_code = 200
                return response
            else:
                mensaje = f'{self.model.__name__} no se ha podido actualizar!'
                error = form.errors
                response = JsonResponse({'mensaje':mensaje, 'error':error})
                response.status_code = 400
                return response
        else:
            return redirect('usuario:inicio_usuarios')

class EliminarUsuario(LoginYSuperStaffMixin, ValidarPermisosMixin, DeleteView):
    model = Usuario
    template_name ='usuarios/eliminar_usuario.html'
    permission_required = ('usuario.view_usuario', 'usuario.add_usuario', 'usuario.change_usuario', 'usuario.delete_usuario')

    def delete(self, request, *args, **kwars):
        if request.is_ajax():
            usuario = self.get_object()
            usuario.usuario_activo = False
            usuario.save()
            mensaje = f'{self.model.__name__} eliminado correctamente!'
            error = 'No hay error!'
            response = JsonResponse({'mensaje':mensaje, 'error':error})
            response.status_code = 200
            return response
        else:
            return redirect('usuario:inicio_usuarios')

