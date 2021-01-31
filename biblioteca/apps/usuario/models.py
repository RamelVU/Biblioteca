from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class UsuarioManager(BaseUserManager):
    """Forma antigua de crear usuarios sin usar PermissionMixins
    def create_user(self, email, username, nombres, password = None):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')

        usuario = self.model(
            username = username, 
            email = self.normalize_email(email), 
            nombres = nombres,
        )

        usuario.set_password(password)
        usuario.save()
        return usuario

    def create_superuser(self, email, username, nombres, password):
        usuario = self.create_user(
            email,
            username = username,
            nombres = nombres,
            password=password
        )

        usuario.usuario_administrador = True
        usuario.save()
        return usuario """

    def _create_user(self, username, email, nombres, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            username = username,
            email = email,
            nombres = nombres,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user
    
    def create_user(self, username, email, nombres, password = None, **extra_fields):
        return self._create_user(username, email, nombres, password,False, False, **extra_fields)
    
    def create_superuser(self, username, email, nombres, password = None, **extra_fields):
        return self._create_user(username, email, nombres, password,True, True, **extra_fields)



class Usuario(AbstractBaseUser, PermissionsMixin):
    username = models.CharField("Nombre de Usuario", unique=True, max_length=100)
    email = models.EmailField("Correo Electrónico", unique=True, max_length=254)
    nombres = models.CharField("Nombres", max_length=200, blank=True, null=True)
    apellidos = models.CharField("Apellidos", max_length=200, blank=True, null=True)
    imagen = models.ImageField("Imagen de Perfil", upload_to='perfil/', max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UsuarioManager()


    USERNAME_FIELD = 'username' #Define el campo que va a requerir parsa la autenticación, suele ser username o email
    REQUIRED_FIELDS = ['email', 'nombres'] #Campos que va a pedir si o si para autenticarse por consola

    class Meta:
        permissions = [('permiso_desde_codigo', 'Esto es un permiso creado desde código'),
                        ('segundo_permiso_codigo', 'Esto es un permiso creado desde código')]#Para que estos permisos se guarden tengo que hacer las migraciones

    def __str__(self):
        return f'{self.nombres} {self.apellidos}'

    # def has_perm(self, perm, obj = None): #tiene que definirse para poder utlizar el modelo usuario en el admin de django
    #     return True

    # def has_module_perms(self, app_label): #igual para el admin de django
    #     return True

    # @property
    # def is_staff(self):
    #     return self.usuario_administrador
