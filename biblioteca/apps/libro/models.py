import datetime
from datetime import timedelta
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, pre_save
from apps.usuario.models import Usuario

# Create your models here.

class Autor(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length = 50, blank = False, null = False)
    apellido = models.CharField(max_length = 50, blank = False, null =False)
    nacionalidad = models.CharField(max_length = 50, blank = False, null =False)
    descripcion = models.TextField(blank = False, null= False)
    estado = models.BooleanField('Estado', default = True)
    fecha_creacion = models.DateField('Fecha de creación', auto_now=True, auto_now_add=False)

    # def clean(self):
    #     if self.nombre.lower() == 'flor':
    #         raise ValidationError('No puedes agregar alguien llamado Flor')

    # def save(self, *args, **kwargs):
    #     if self.nombre.lower() == 'flor':
    #         raise ValidationError('No puedes agregar alguien llamado Flor')
    #     super(Autor, self).save(*args, **kwargs)

    

    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'
        ordering = ['id']

    def natural_key(self):
        return f'{self.nombre} {self.apellido}'

    def __str__(self):
        return self.nombre

class Libro(models.Model):
    id = models.AutoField(primary_key = True)
    titulo = models.CharField('Título', max_length = 255, blank = False, null = False)
    fecha_publicacion = models.DateField('Fecha de publicación', blank = False, null = False)
    descripcion = models.TextField('Descripcion', blank = True, null= True)
    cantidad = models.SmallIntegerField('Cantidad o Stock', default=1)
    imagen = models.ImageField('Imagen', upload_to='libros/', max_length=255, null=True, blank=True)
    autor_id = models.ManyToManyField(Autor)
    estado = models.BooleanField('Estado', default = True)
    fecha_creacion = models.DateField('Fecha de creación', auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'
        ordering = ['titulo']

    def __str__(self):
        return self.titulo

    def natural_key(self):
        return f'{self.titulo}'

    def obtener_autores(self):
        # autores = str([autor for autor in self.autor_id.all().values_list('nombre', flat=True)]).replace("[",'').replace("]",'').replace("'",'')
        autores = self.autor_id.all()
        autores_list = ''
        for autor in autores:
            if autor.id == autores[len(autores)-1].id:   
                autores_list += autor.nombre
            else:
                autores_list += autor.nombre+', '
        return autores_list

class Reserva(models.Model):
    id = models.AutoField(primary_key=True)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    cantidad_dias = models.SmallIntegerField('Cantidad de días a reservar', default=7)
    estado = models.BooleanField('Estado', default = True)
    fecha_creacion = models.DateField('Fecha de creación', auto_now_add=True)
    fecha_vencimiento = models.DateField('Fecha de vencimiento', auto_now=False, auto_now_add=False, null=True, blank=True)

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'

    def __str__(self):
        return f'Reserva de libro {self.libro} por {self.usuario}'

    def save(self, *args, **kwargs):
        if self.fecha_creacion == None:
            self.fecha_vencimiento = datetime.date.today() + timedelta(days = self.cantidad_dias)
        else:
            self.fecha_vencimiento = self.fecha_creacion + timedelta(days = self.cantidad_dias)
        super().save(*args, **kwargs)

def quitar_relacio_autor_libro(sender, instance, **kwargs):
    if instance.estado == False:
        autor = instance.id
        libros = Libro.objects.filter(autor_id = autor)
        for libro in libros:
            libro.autor_id.remove(autor)

def reducir_cantidad_libro(sender,instance, **kwargs):
    libro = instance.libro
    if libro.cantidad > 0:
        libro.cantidad -= 1
        libro.save()

def validad_creacion_reserva(sender, instance, **kwargs):
    libro = instance.libro
    if libro.cantidad < 1:
        raise Exception("No puede realizar esta reserva")

def agregar_fecha_vencimiento_reserva(sender,instance,**kwargs):
    if instance.fecha_vencimiento is None or instance.fecha_vencimiento == '':
        instance.fecha_vencimiento = instance.fecha_creacion + timedelta(days = instance.cantidad_dias)
        instance.save()

post_save.connect(quitar_relacio_autor_libro, sender = Autor)
post_save.connect(reducir_cantidad_libro, sender = Reserva)
# pre_save.connect(validad_creacion_reserva, sender = Reserva)
# post_save.connect(agregar_fecha_vencimiento_reserva,sender = Reserva)