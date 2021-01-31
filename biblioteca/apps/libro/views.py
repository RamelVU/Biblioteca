from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import AutorForm, LibroForm
from .models import *
from django.views.generic import View, TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from apps.usuario.mixins import LoginMixin

# Create your views here.

    # def home(request):
    #     return render(request, 'index.html') 

    # class Inicio(View):
    #     def get(self, request, *arg, **kwarg):
    #         return render(request, 'index.html')


    # def listarAutor(request):
    #     autores = Autor.objects.filter(estado = True)
    #     return render(request, 'libro/listar_autores.html', {'autores': autores})


    # def crearAutor(request):
        
    #     if request.method == 'POST':
    #         autor_form = AutorForm(request.POST)
    #         if autor_form.is_valid():
    #             autor_form.save()
    #             return redirect('index')
    #     else:
    #         autor_form = AutorForm()
    #     return render(request, 'libro/crear_autor.html', {'autor_form':autor_form}) 

    # def editarAutor(request, id):

    #     autor_form = None
    #     error = None
    #     try:
    #         autor = Autor.objects.get(id = id)
    #         if request.method == 'GET':
    #             autor_form = AutorForm(instance = autor)
    #         else:
    #             autor_form = AutorForm(request.POST, instance = autor)
    #             if autor_form.is_valid():
    #                 autor_form.save()
    #                 return redirect('index')
    #     except ObjectDoesNotExist as e:
    #         error = e

    #     return render(request, 'libro/crear_autor.html', {'autor_form': autor_form, 'error':error})

    # def eliminarAutor(request, id):

    #     autor = Autor.objects.get(id = id)
        
    #     if request.method == 'POST':
    #         #autor.delete() ---> Para eliminar de forema logica
    #         autor.estado = False
    #         autor.save()
    #         return redirect('libro:listar_autor')
        
    #     return render(request, 'libro/eliminar_autor.html', {'autor':autor})

class ListadoAutores(View):
    model = Autor

    def get_queryset(self):
            return self.model.objects.filter(estado=True)
    
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = serialize('json', self.get_queryset())
            return HttpResponse(data, 'application/json')
        return redirect('libro:listado_autores')

class CrearAutor(CreateView):
    model = Libro
    template_name = 'libro/autor/crear_autor.html'
    form_class = AutorForm

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            
            form = self.form_class(request.POST)    
            if form.is_valid():
                form.save()
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
            return redirect('libro:listado_autores')

class EditarAutor(UpdateView):
    model = Autor
    template_name = 'libro/autor/editar_autor.html'
    form_class = AutorForm

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            
            form = self.form_class(request.POST, instance=self.get_object())    
            if form.is_valid():
                form.save()
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
            return redirect('libro:listado_autores')

class EliminarAutor(DeleteView):
    model = Autor
    template_name ='libro/autor/eliminar_autor.html'

    def delete(self, request, *args, **kwars):
        if request.is_ajax():
            autor = self.get_object()
            autor.estado = False
            autor.save()
            mensaje = f'{self.model.__name__} eliminado correctamente!'
            error = 'No hay error!'
            response = JsonResponse({'mensaje':mensaje, 'error':error})
            response.status_code = 200
            return response
        else:
            return redirect('usuario:inicio_usuarios')


class ListadoLibros(ListView):
    model = Libro

    def get_queryset(self):
        return self.model.objects.filter(estado=True)
    
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = serialize('json', self.get_queryset(), use_natural_foreign_keys = True)
            return HttpResponse(data, 'application/json')
        return redirect('libro:listado_libros')

class CrearLibro(CreateView):
    model = Libro
    template_name = 'libro/libro/crear_libro.html'
    form_class = LibroForm

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            
            form = self.form_class(data = request.POST, files = request.FILES)    
            if form.is_valid():
                # nuevo_libro = Libro(titulo = form.cleaned_data['titulo'],
                #     fecha_publicacion = form.cleaned_data['fecha_publicacion'],
                #     autor_id = form.cleaned_data['autor_id']
                # )
                form.save()
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
            return redirect('libro:listado_libros')

class EditarLibro(UpdateView):
    model = Libro
    template_name = 'libro/libro/editar_libro.html'
    form_class = LibroForm

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            
            form = self.form_class(data = request.POST, files = request.FILES, instance=self.get_object())    
            if form.is_valid():
                form.save()
                mensaje = f'{self.model.__name__} actualizado correctamente!'
                error = 'No hay error!'
                response = JsonResponse({'mensaje':mensaje, 'error':error})
                response.status_code = 200
                return response
            else:
                mensaje = f'{self.model.__name__} no se ha podido registrar!'
                error = form.errors
                response = JsonResponse({'mensaje':mensaje, 'error':error})
                response.status_code = 400
                return response
        else:
            return redirect('libro:listado_libros')

class EliminarLibro(DeleteView):
    model = Libro
    template_name ='libro/libro/eliminar_libro.html'

    def delete(self, request, *args, **kwars):
        if request.is_ajax():
            libro = self.get_object()
            libro.estado = False
            libro.save()
            mensaje = f'{self.model.__name__} eliminado correctamente!'
            error = 'No hay error!'
            response = JsonResponse({'mensaje':mensaje, 'error':error})
            response.status_code = 200
            return response
        else:
            return redirect('usuario:inicio_usuarios')


class ListadoLibrosDisponibles(LoginMixin, ListView):
    model = Libro
    paginate_by = 6
    template_name = 'libro/libro/libros_disponibles.html'
    
    def get_queryset(self):
        queryset = self.model.objects.filter(estado=True, cantidad__gte = 1)
        return queryset

class ListadoLibrosReservados(LoginMixin, ListView):
    model = Reserva
    template_name = 'libro/libro/libros_reservados.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(estado = True, usuario=self.request.user)
        return queryset

class Reservas(LoginMixin, ListView):
    model = Reserva

    def get_queryset(self):
        return self.model.objects.filter(estado=True, usuario=self.request.user)
    
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = serialize('json', self.get_queryset(), use_natural_foreign_keys = True)
            return HttpResponse(data, 'application/json')
        return redirect('libro:listado_libros_reservados')

class ReservasVencidas(LoginMixin, ListView):
    model = Reserva

    def get_queryset(self):
        return self.model.objects.filter(estado=False, usuario=self.request.user)
    
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = serialize('json', self.get_queryset(), use_natural_foreign_keys = True)
            return HttpResponse(data, 'application/json')
        return redirect('libro:listado_reservas_vencidas')

class DetalleLibroDisponible(LoginMixin, DetailView):
    model = Libro
    template_name = 'libro/libro/detalle_libro.html'

    def get(self, request, *args, **kwargs):
        if self.get_object().cantidad > 0:
            return render(request, self.template_name, {'object': self.get_object()})
        return redirect('libro:listado_libros_disponible')

    # def get_object(self):
    #     try:
    #         instance = self.model.objects.filter(id = self.kwargs['pk'])
    #     except:
    #         pass
    #     return instance

    # def get_context_data(self, **kwargs):
    #     context = {}
    #     context['object'] = self.get_object()
    #     return context

    # def get(self, request, *args, **kwargs):
    #     return render(request, self.template_name, self.get_context_data())

class RegistrarReserva(LoginMixin, CreateView):
    model = Reserva
    success_url = reverse_lazy('libro:listado_libros_disponible')

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            libro = Libro.objects.filter(id = request.POST.get('libro')).first()
            usuario = Usuario.objects.filter(id = request.POST.get('usuario')).first()
            if libro and usuario:
                if libro.cantidad > 0:
                    nueva_reserva = self.model(
                        libro = libro,
                        usuario = usuario
                    )
                    nueva_reserva.save()
                    mensaje = f'{self.model.__name__} registrado correctamente!'
                    error = 'No hay error!'
                    response = JsonResponse({'mensaje':mensaje, 'error':error, 'url': self.success_url})
                    response.status_code = 201
                    return response
        return redirect('libro:listado_libros_disponible')
