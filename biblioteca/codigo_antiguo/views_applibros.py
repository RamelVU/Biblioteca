from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from .forms import AutorForm, LibroForm
from .models import Autor, Libro
from django.views.generic import View, TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

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

class Inicio(TemplateView):
    template_name = 'index.html'


class ListadoAutores(View):
    model = Autor
    form_class = AutorForm
    template_name = 'libro/autor/listar_autores.html'

    def get_queryset(self):
            return self.model.objects.filter(estado=True)

    def get_context_data(self, **kwargs):
        contexto = {}
        contexto['autores'] = self.get_queryset()
        contexto['form'] = self.form_class
        return contexto
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return redirect('libro:listar_autor')

# class CrearAutor(CreateView):
#     model = Autor
#     template_name = 'libro/autor/crear_autor.html'
#     form_class = AutorForm
#     success_url = reverse_lazy('libro:listar_autor')

class EditarAutor(UpdateView):
    model = Autor
    template_name = 'libro/autor/listar_autores.html'
    form_class = AutorForm
    success_url = reverse_lazy('libro:listar_autor')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['autores'] = Autor.objects.filter(estado=True)
        return context

class EliminarAutor(DeleteView):
    model = Autor
    success_url = reverse_lazy('libro:Listar_autor')

    def post(self, request,pk, *args, **kwargs):
        object = Autor.objects.get(id = pk)
        object.estado = False
        object.save()
        return redirect('libro:listar_autor')


class ListadoLibros(View):
    model = Libro
    form_class = LibroForm
    template_name = 'libro/libro/listar_libro.html'

    def get_queryset(self):
        return self.model.objects.filter(estado=True)

    def get_context_data(self, **kwargs):
        contexto = {}
        contexto['libros'] = self.get_queryset()
        contexto['form'] = self.form_class
        return contexto
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

class CrearLibro(CreateView):
    model = Libro
    template_name = 'libro/libro/crear_libro.html'
    form_class = LibroForm
    success_url = reverse_lazy('libro:listar_libro')

class EditarLibro(UpdateView):
    model = Libro
    template_name = 'libro/libro/editar_libro.html'
    form_class = LibroForm
    success_url = reverse_lazy('libro:listar_libro')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['libros'] = Libro.objects.filter(estado=True)
        return context

class EliminarLibro(DeleteView):
    model = Libro
    success_url = reverse_lazy('libro:Listar_autor')

    def post(self, request,pk, *args, **kwargs):
        object = Libro.objects.get(id = pk)
        object.estado = False
        object.save()
        return redirect('libro:listar_libro')
