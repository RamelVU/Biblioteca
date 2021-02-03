from django import forms
from django.core.exceptions import ValidationError
from .models import *

class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        # fields =['nombre', 'apellido', 'nacionalidad', 'descripcion']
        fields =['nombre', 'apellido']
        labels = {
            'nombre': 'Nombre', 
            'apellido': 'Apellidos', 
            'nacionalidad': 'Nacionalidad', 
            'descripcion': 'Descripción'
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ingrese el nombre', }),
            'apellido': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ingrese los apellidos', }), 
            # 'nacionalidad': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ingrese la nacionalidad', 'id':'nacionalidad'}), 
            # 'descripcion': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Ingrese la descripcion', 'id':'descripcion'})
        }

class LibroForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['autor_id'].queryset = Autor.objects.filter(estado=True)

    class Meta:
        model = Libro
        fields =['titulo', 'fecha_publicacion', 'autor_id', 'descripcion', 'imagen', 'cantidad']
        labels = {
            'titulo': 'Título', 
            'fecha_publicacion': 'Fecha de Publicación', 
            'autor_id': 'Autor', 
            'cantidad': 'Cantidad en stock',
            'descripcion': 'Descripción',
            'imagen': 'Imagen'
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ingrese título del libro', 'id':'titulo'}),
            'fecha_publicacion': forms.SelectDateWidget(attrs={'class':'form-control', 'id':'fecha_publicacion'}),
            'autor_id': forms.SelectMultiple(attrs={'class':'form-control', 'id':'autor_id'}),
            'descripcion': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Ingrese la descripcion', 'id':'descripcion'}),
            'cantidad': forms.NumberInput(attrs={'class':'form-class', 'placeholder':'Ingrese la cantidad de libros en stock', 'id':'cantidad'})
        }

class ReservaForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['libro'].queryset = Libro.objects.filter(estado=True, cantidad__gte = 1)

    class Meta:
        model = Reserva
        fields = '__all__'
    
    def clean_libro(self):
        libro = self.cleaned_data['libro']
        if libro.cantidad < 1:
            raise ValidationError('No se puede reservar este libro, deben existir unidades disponibles')

        return libro