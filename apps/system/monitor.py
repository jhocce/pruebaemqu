import jwt
import uuid 
import time
import json
from django.apps import apps
from django.conf import settings
from rest_framework.response import Response
from django.http import HttpResponse
from django.db.models import Q, F
from apps.system.ManageApi import ErrorManagerMixin
from datetime import datetime
from apps.user.models import user, Token
from django.core.paginator import Paginator

from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from dateutil import tz

class ErrorMonitor(Exception):
    pass

class MonitorMixin(ErrorManagerMixin):
	""" Clase que hereda de ErrorManagerMixin y es encargada de
		monitorear y controlodar los accesos del usuario a las 
		peticiones al sistema

	  """
	estado = False
	def dispatch(self, request, *args, **kwargs):
		
		self.pk_publica = request.GET.get('pk')
		self.count = request.GET.get('count')
		self.page = request.GET.get('page')
		if self.count==None:
			self.count=100
		if self.page==None:
			self.page=1
		self.criterios = request.GET.get('filter')
		if self.valid_token(request=request) is False:
			
			return HttpResponse( json.dumps(self.salida()) , status=303)
		return super(MonitorMixin, self).dispatch(request,*args, **kwargs )

	def valid_token(self, request):

		try:
			# print(request.headers['Authorization'])
			try:
			
				tokenJWTENCODE = request.headers['Authorization']
			except Exception as e:
				self.MensajeListAdd( mensaje_user = 'No autorizado',
					mensaje_server="No autorizado",
					status= 303)
			tokenJWTDECODE = jwt.decode(tokenJWTENCODE, settings.SECRET_KEY_TOKEN , algorithms="HS256")
			
			token = tokenJWTDECODE['token']
			utc = tz.tzutc()
			local = tz.tzlocal()
			try:
				token = Token.objects.get(token=token)
			except Exception as e:
				self.MensajeListAdd( mensaje_user = 'Su sesion a expirado',
					mensaje_server=str(e),
					status= 401)

				return False
				
			  
			fecha2 = datetime.now()


			fecha1 = token.Modificado.replace(tzinfo=utc)
			fecha1 = fecha1.astimezone(local)

			diferencia = time.mktime(fecha2.timetuple()) - time.mktime(fecha1.timetuple()) 
			if diferencia > (60*60):

				self.MensajeListAdd( mensaje_user = 'Su sesion a expirado', status=401)
				token.Status = False
				token.save()
				return False
			else:
				token.Modificado = datetime.now()
				token.save()
				permisos = token.user.Tipo
				self.usuario =  token.user
				p = self.GetModel()
				try:
					print(request.method.lower(), permisos)
					if request.method.lower() in p.permisos()[permisos]:
						return True
					else:
						self.MensajeListAdd( mensaje_user = 'El token no posee permisos adecuados para esta acción', 
							mensaje_server='El token no posee permisos adecuados para esta acción', status=303)
						return False
				except Exception as e:
					# print(p)
					self.MensajeListAdd( mensaje_user = 'Ocurrio un error al procesar la solicitud', 
							mensaje_server='El modelo "{0}" No tiene la función: permisos()'.format(self.GetModel().__name__), status=303)
					return False
				
		except Exception as e:
			print(e)
			self.MensajeListAdd( mensaje_server = str(e), status=500)

			return False

	def detallestoken(self, token):

		try:
			# print(token)
			utc = tz.tzutc()
			local = tz.tzlocal()
			token = Token.objects.get(token=token)
			
			fecha2 = datetime.now()

			ultima_peticion = str(token.Modificado)
			fecha1 = token.Modificado.replace(tzinfo=utc)
			fecha1 = fecha1.astimezone(local)

			diferencia = time.mktime(fecha2.timetuple()) - time.mktime(fecha1.timetuple()) 

			if diferencia > (60*60):

				self.MensajeListAdd( mensaje_user = 'Su sesion a expirado')
				token.Status = False
				token.save()
				return False
			else:
				token.Modificado = datetime.now()
				token.save()
				permisos = token.user.Tipo

				self.JsonAdd(json = {
					'ambito': permisos,
					'ultima_peticion':ultima_peticion,
					'Status': token.Status,
					'usuario': token.user.username,
					})

				return False
		except Exception as e:
			# print(e)
			self.MensajeListAdd( mensaje_server = str(e))
			return False

	


	def get_object(self):
		try:
			objeto = self.model.objects.filter(Q(pk_publica=self.pk_publica)&Q(user=self.usuario)&Q(Status=True)).first()
			return objeto
		except Exception as e:
			raise e

	def get_user(self):
		return self.usuario
	def get_queryset(self):
		if self.criterios != None:
			query =  self.model.objects.filter(Q(user=self.usuario)&Q(Status=True))
			campos = self.model._meta.get_fields()

			models = {
			    model.__name__: model for model in apps.get_models()
			}
			campos = [Fila.name for Fila in campos]
			campos.remove('user')
			print(campos)
			condiciones = ''
			lis = []
			argdict = json.loads(self.criterios.encode('utf-8'))
			for x in argdict.keys():
				if "_" in x:
					print(x)
					modelo = x.split("_")[0]
					print(modelo)
					print(models.keys())
					if modelo in models.keys():
						print(argdict[x])
						# print("modelo capturado")
						p = models[modelo].objects.get(pk_publica=argdict[x])
						print("---------------------")
						print(p.id.value_to_string)
						print(dir(p.id))
						if modelo in campos:
							campos.remove(modelo)
							if condiciones != '':
								condiciones = condiciones + 'and ("{0}"={1})'.format(x, p.id )
							else:
								condiciones = condiciones + '("{0}"={1})'.format(x, p.id )
							lis.append(x)
			for modelo in lis:
				del argdict[x]
			# print(argdict)
			i = 0
			for x in argdict.keys():
				i = i+1
				if x in campos:
					if i >1:
						condiciones = condiciones + " and ({0}='{1}')".format(x, argdict[x])
					else:
						condiciones = condiciones + "({0}='{1}')".format(x, argdict[x])
				else:
					raise Exception('El criterio "{0}" enviado en la peticion no se encuentra en estos registros'.format(x))
			sql = 'SELECT * FROM {0}_{1} WHERE {2}'.format(self.model._meta.app_label, self.model._meta.model_name, condiciones)
			print(sql)
			try:
				# print(sql)
				q = query.raw(sql)

			except Exception as e:
				# print("-------------------------------",e)
				raise Exception('Error desconocido: {0} '.format(e))

			return q
		else:
			con = self.model.objects.filter(Q(user=self.usuario)&Q(Status=True))

			if self.count and self.page:
				paginacion= Paginator(con,self.count)
				
				if len(paginacion.page(1)) == 0:
					return None
				else:
					con= paginacion.page(self.page)
			return con
		

	def	get_querysetall(self):
		return self.model.objects.filter(Status=True)
	def get_objectabsolute(self):
		try:
			objeto = self.model.objects.filter(Q(pk_publica=self.pk_publica)&Q(Status=True)).first()
			return objeto
		except Exception as e:
			raise e
