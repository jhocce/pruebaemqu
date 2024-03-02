import uuid
from django.db import models
from apps.system.models import basemodel
from apps.user.models import user

# Create your models here.
class Equipo(basemodel):

    Nombre  = models.CharField(max_length=100, default="")
    direccion = models.CharField(max_length=20)
 
    Tipos=(
	  ('Ejecutando','Ejecutando'),
	  ('Inactivo','Inactivo'))
	 
    servicio = models.CharField(max_length=50, choices=Tipos, default='Inactivo')
    paquetes = models.IntegerField(default=0)

    user = models.ForeignKey(user,
								related_name="userequipo", 
								null=True, 
								blank=True, 
								on_delete=models.CASCADE)

    def __str__(self):
        return self.Nombre +" : "+ self.direccion
    def permisos():

        permisos = {
			'admin' : ('get','post','put', 'delete'),
			'standar' : ('get','post','put', 'delete'),
			'servicio' : ('get','post','put', 'delete'),
		}
        return permisos
	
class Test(basemodel):

    responde = models.BooleanField(default=False)
    enviados  = models.IntegerField(default=0)
    recibidos  = models.IntegerField(default=0)
    perdidos  = models.IntegerField(default=0)
    maximo  = models.IntegerField(default=0)
    media  = models.IntegerField(default=0)
    minimo  = models.IntegerField(default=0)

    equipo = models.ForeignKey(Equipo,
								related_name="test",
								null=True, 
								blank=True, 
								on_delete=models.CASCADE)
    
    def permisos():

        permisos = {
			'admin' : ('get','post','put', 'delete'),
			'standar' : ('get','post','put', 'delete'),
			'servicio' : ('get','post','put', 'delete'),
		}
        return permisos
    

