from django.shortcuts import render

# Create your views here.
from django.db.models import Q, F
from ast import literal_eval
from django.http import Http404
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.system.monitor import MonitorMixin
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from .serializers import EquipoSerializer, TestSerializer
from .models import Equipo, Test
from apps.system.action import service




class EquipoAPI(MonitorMixin,CreateAPIView, ListAPIView, 
	RetrieveAPIView, UpdateAPIView, DestroyAPIView, APIView):
	
	serializer_class = EquipoSerializer
	model = Equipo
	
	def update(self, request, *arg, **kwargs):
		try:
			if self.pk_publica is None:
				self.MensajeListAdd(mensaje_user='Ocurrieron errores al momento de guardar el Equipo',
				mensaje_server='No se a enviado correctamente la variable "pk" correspondiente al objeto a actualizar en la URL', status='error')
				return Response(self.salida(), status=303)
			else:
				try:
					print(self.get_user())
					objeto = self.model.objects.get(pk_publica=self.pk_publica, 
						user=self.get_user(), 
						Status=True )
				except self.model.DoesNotExist:
					self.MensajeListAdd(mensaje_user = 'Ocurrieron uno o mas errores a actualizar el Equipo',
						mensaje_server = 'El objeto no existe o no pertenece al usuario al que esta relacionado al token')
					return Response(self.salida(), status=404)
				
				EquipoSerializer = self.serializer_class( objeto, data= request.data)
				if EquipoSerializer.is_valid():
					EquipoSerializer.save()
					self.MensajeListAdd(mensaje_user='Equipo guardado con exito', status='success')
					self.JsonAdd(json = EquipoSerializer.data )
					return Response( self.salida(), status=200)
				else:
					self.JsonAdd(json = EquipoSerializer.errors )
					self.MensajeListAdd(mensaje_user='Ocurrieron errores al momento de guardar el Equipo',
						mensaje_server=EquipoSerializer.errors, status='error')

					return Response(self.salida(), status=200)
		except Exception as e:
			self.MensajeListAdd(mensaje_server  = str(e))
			return Response(self.salida(), status=500)
		
	def post(self, request, *arg, **kwargs):
		try:
			
			EquipoSerializer = self.serializer_class(data= request.data)
			
			if EquipoSerializer.is_valid():
				EquipoSerializer.validated_data['user'] = self.get_user()
				EquipoSerializer.save()
				self.MensajeListAdd(mensaje_user='Equipo guardado con exito', status='success')
	
				data = dict(EquipoSerializer.data)
				data['pk_publica'] = EquipoSerializer.instance.pk_publica
				self.JsonAdd(json = data )
				return Response( self.salida(), status=200)

			else:
				self.JsonAdd(json = EquipoSerializer.errors )
				self.MensajeListAdd(mensaje_user='Ocurrieron errores al momento de guardar el Equipo',
					mensaje_server=EquipoSerializer.errors, status='error')
				return Response(self.salida(), status=200)

		except Exception as e:
			self.MensajeListAdd(mensaje_server  = str(e))
			return Response(self.salida(), status=500)
		
	def get(self, request, *arg, **kwargs):

		try:
			usuario = self.get_user()	
			if self.pk_publica is None:

				quey = self.get_queryset()
				if quey is not None:
					total_count = quey.object_list.count()
					f = self.serializer_class(quey, many=True)
					
					
					self.JsonAdd(json={
						"total_count":total_count,
						"data":f.data
						})
				else:
					self.MensajeListAdd(mensaje_user = 'No hay registros')
				return Response(self.salida(), status=200)
			else:
				quey = self.get_object()
				if quey is None:
					self.MensajeListAdd(mensaje_user = 'El Equipo no existe',
						mensaje_server = 'El Equipo no existe o no pertenece al usuario relacionado con el token')			
					return Response(self.salida(), status=200)
				else:
					f = self.serializer_class(quey)
					self.JsonAdd(json=f.data)			
					return Response(self.salida(), status=200)

		except Exception as e:
			self.MensajeListAdd(mensaje_server  = str(e))
			return Response(self.salida(), status=500)

	def delete(self, request, *arg, **kwargs):
		
		try:
			objeto = self.get_object()
			objeto.Status = False
			objeto.save()
			self.MensajeListAdd(mensaje_user = 'El Equipo a sido eliminado exitosamente')
		except Exception as e:
			self.MensajeListAdd(mensaje_server  = str(e))
			
		

		return Response(self.salida(), status=200)
	

class TestAPI(MonitorMixin,ListAPIView, APIView):
	
	serializer_class = TestSerializer
	model = Test
	
	def get(self, request, pk, *arg, **kwargs):

		try:
       
			registros = self.model.objects.get(Equipo__pk_publica=pk)
			if registros is not None:
				f = self.serializer_class(registros, many=True)
				self.JsonAdd(json=f.data)
			else:
				self.MensajeListAdd(mensaje_user = 'No hay registros')
			return Response(self.salida(), status=200)
		except Exception as e:
			self.MensajeListAdd(mensaje_server  = str(e))
			return Response(self.salida(), status=500)
    
    

class TesttestAPI(MonitorMixin, APIView):
	
	serializer_class = TestSerializer
	model = Test
	
	def post(self, request, *arg, **kwargs):

		try:
			pk = request.GET.get('pk')
			try:
				equipo = Equipo.objects.get(pk_publica=pk)
			except Exception as e:
				print(e)
			
			
			b = service(equipo=equipo)
			b.start()
			# b.join()
			equipo.servicio = "Ejecutando"
			equipo.save()
			self.MensajeListAdd(mensaje_user = 'Ejecutando en segundo plano')
			return Response(self.salida(), status=200)
		except Exception as e:
			print("dasd")
			self.MensajeListAdd(mensaje_server  = str(e))
			return Response(self.salida(), status=500)
    