
from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    path('listar_autores/',login_required(ListadoAutores.as_view()), name = 'listar_autores'),
    path('crear_autor/',login_required(CrearAutor.as_view()), name = 'crear_autor'),
    path('editar_autor/<int:pk>/',login_required(EditarAutor.as_view()), name = 'editar_autor'),
    path('eliminar_autor/<int:pk>/',login_required(EliminarAutor.as_view()), name = 'eliminar_autor'),

    path('listar_libro/',login_required(ListadoLibros.as_view()), name = 'listar_libro'),
    path('crear_libro/',login_required(CrearLibro.as_view()), name = 'crear_libro'),
    path('editar_libro/<int:pk>/',login_required(EditarLibro.as_view()), name = 'editar_libro'),
    path('eliminar_libro/<int:pk>/',login_required(EliminarLibro.as_view()), name = 'eliminar_libro'),

    #URLs Generales
    path('reservas/', Reservas.as_view(), name = 'reservas'),
    path('listar-libros-disponibles/',ListadoLibrosDisponibles.as_view(), name = 'listado_libros_disponible'),
    path('detalle-libro/<int:pk>',DetalleLibroDisponible.as_view(), name = 'detalle_libro'),
    path('listar-libros-reservados/',ListadoLibrosReservados.as_view(), name = 'listado_libros_reservados'),
    path('reservar-libro/',RegistrarReserva.as_view(), name = 'reservar_libro'),
    path('reservas-vencidas/',ReservasVencidas.as_view(), name = 'reservas_vencidas'),
]

# URLs DE VISTAS IMPLICITAS
urlpatterns += [
    path('listado_libros/', login_required(TemplateView.as_view(template_name = 'libro/libro/listar_libros.html')), name='listado_libros'),
    path('listado_autores/', login_required(TemplateView.as_view(template_name = 'libro/autor/listar_autores.html')), name='listado_autores'),
    path('listar-reservas-vencidas/',TemplateView.as_view(template_name = 'libro/libro/reservas_vencidas.html'), name = 'listado_reservas_vencidas'),
]