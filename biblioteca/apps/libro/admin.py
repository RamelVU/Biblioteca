from django.contrib import admin
from .models import*
from.forms import ReservaForm

class ReservaAdmin(admin.ModelAdmin):
    form = ReservaForm
    list_display = ('libro', 'usuario', 'fecha_creacion', 'fecha_vencimiento', 'estado')


class AutorAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'apellido', 'nacionalidad')
    list_display = ('nombre', 'apellido', 'nacionalidad', 'estado')
    actions = ['eliminacion_logica_autores', 'activacion_logica_autores']

    def eliminacion_logica_autores(self, request, queryset):
        for autor in queryset:
            autor.estado = False
            autor.save()

    def activacion_logica_autores(self, request, queryset):
        for autor in queryset:
            autor.estado = True
            autor.save()

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

# Register your models here.

admin.site.register(Autor, AutorAdmin)
admin.site.register(Libro)
admin.site.register(Reserva, ReservaAdmin)
