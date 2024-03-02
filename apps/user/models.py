import uuid
from django.db import models
from apps.system.models import basemodel

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin



	

class UserManager(BaseUserManager):
	""" Modelo que hereda de la clase base que usa django para generar 
	los usuarios, de esta forma podemos personalizar los campos 
	necesarios para generar el usuario que creamos en la consola
	con el comando "python manage.py createsuperuser" """

	def _create_user(self, email, password, 
					is_staff, is_superuser, **extra_field):

		if not email:
			raise ValueError("El campo email es necesario")
		email = self.normalize_email(email)
		user = self.model(email=email, is_active=True, is_staff=is_staff,
							is_superuser=is_superuser, **extra_field)
		user.set_password(password)
		user.save(using = self._db)

		return user

	def create_user(self, email, password=None, **extra_field):
		return self._create_user(email, password, False, False,  **extra_field)

	def create_superuser(self, email, password, **extra_field):
		return self._create_user(email, password, True, True,  **extra_field)

class user(AbstractBaseUser, PermissionsMixin):

	""" Modelo usado para generar al usuario que se maneja en el contexto de la
	plataforma.
	Hereda propiedades de  AbstractBaseUser  y PermissionsMixin para que el modelo
	a pesar de ser personalizado pueda ser usado por django en sus subrutinas de 
	verificación y validación. """

	pk_publica = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	Creado = models.DateTimeField(auto_now_add=True)
	Modificado =models.DateTimeField(auto_now=True)
	username = models.CharField(max_length=50)
	email = models.EmailField(max_length=50, unique=True)
	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)

	Status = models.BooleanField(default=True)

	Nombres = models.CharField(max_length=50, default="")
	Apellidos = models.CharField(max_length=50, default="")
	Tipos = (('admin','1'), ('standar','2'), ('servicio','3'))
	Tipo = models.CharField(max_length=20, choices=Tipos, default='standar')


	objects = UserManager() 

	USERNAME_FIELD = 'email'

	# REQUIRED_FIELDS = ['email']

	def get_short_name(self):
		return self.username


	def permisos():

		permisos = {
			'admin' : ('get','post','update', 'delete'),
			'standar' : ('get','post','update', 'delete'),
			'servicio' : ('get','post','update', 'delete'),
		}
		return permisos

class Token(basemodel):


	token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	
	user = models.ForeignKey(user,
								related_name="Token", 
								null=True, 
								blank=True, 
								on_delete=models.CASCADE)
	def permisos():

		permisos = {
			'admin' : ('get','post','update', 'delete'),
			'standar' : ('get','post'),
			'servicio' : ('get','post'),
		}

		return permisos