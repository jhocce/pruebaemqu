from django.shortcuts import render

# Create your views here.
import jwt
from django.db.models import Q
from django.db.models import F
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.http.response import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.views.generic import FormView, View, RedirectView
from django.views.generic import DetailView, CreateView, UpdateView

from .forms import DatosUsuarioForm
from apps.system.models import login
from apps.system.monitor import MonitorMixin
from apps.system.ManageApi import ErrorManagerMixin
from .models import user, Token
from .serializers import UsuarioSerializer, LoginSerializer


from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings



class LogoutUserApi(ErrorManagerMixin, APIView):


	def post(self, request, *arg, **kwargs):

		token = request.data['token']

		try:
			token = Token.objects.get(token=token)
			token.Status = False
			token.save()
			self.MensajeListAdd(mensaje_user = 'Sesion finalizada')

		except Exception as e:
			self.MensajeListAdd( mensaje_server = str(e))
			return Response(self.ErrorList(), status=404)
		
		return Response(self.ErrorList(), status=200)

class LoginUserAPI(ErrorManagerMixin, APIView):

	serializer_class = LoginSerializer
	model = login

	def post(self, request, *arg, **kwargs):

		e = ''
		if request.data['email'] is None:
			self.MensajeListAdd( mensaje_user = 'Ocurrio un error al procesar la solicitud', 
							mensaje_server='No estas enviando correctamente el email')
			return Response(self.salida(), status=500)

		if request.data['password'] is None:
			self.MensajeListAdd( mensaje_user = 'Ocurrio un error al procesar la solicitud', 
							mensaje_server='No estas enviando correctamente el password')
			return Response(self.salida(), status=500)
		
		email =  request.data['email']
		password =  request.data['password']
		print(email, password)
		try:
			usermodel = user.objects.filter(Q(email=email)&Q(password=password))
			usuario = usermodel.first()
			if usermodel.count() == 0:
				self.MensajeListAdd(mensaje_user = 'Usuario o Contraseña invalida')
				return Response(self.salida(), status=404)
			else:
				try:
					tokens = Token.objects.filter(user =  usuario, Status=True)
					# if tokens:
					# 	self.MensajeListAdd(mensaje_user = 'Inicio de sesion correcto')
					for tok in tokens:
						tok.Status = False
						tok.save()

				except Exception as e:
					print(e)
					self.MensajeListAdd(mensaje_server  = str(e))
					return Response(self.salida(), status=500)

					
				token = Token(user = usuario)
				token.save()
				key = settings.SECRET_KEY_TOKEN
				encoded = jwt.encode({'token' : str(token.token)}, key, algorithm="HS256")
				
				jsonresp = {
					'token' : encoded
				}
				self.MensajeListAdd(mensaje_user = 'Inicio de sesion correcto')
				self.JsonAdd(json=jsonresp)
				return Response(self.salida(), status=200)

		except Exception as e:
			self.MensajeListAdd( mensaje_server = str(e))
			return Response(self.salida(), status=500)
			
		
	def __str__(self):
		return 'LoginUserAPI'

class RegisterApi(ErrorManagerMixin, APIView):
	
	model= user
	def post(self, request, *arg, **kwargs):
		if request.data['email'] is None:
			self.MensajeListAdd( mensaje_user = 'Ocurrio un error al procesar la solicitud', 
						mensaje_server='No estas enviando correctamente el username')
			return Response(self.salida(), status=200)

		if request.data['password'] is None:
			self.MensajeListAdd( mensaje_user = 'Ocurrio un error al procesar la solicitud', 
						mensaje_server='No estas enviando correctamente el password')
			return Response(self.salida(), status=200)
		request.data['username'] =request.data['email']

		UsuarioSerializerresponse = UsuarioSerializer(data= request.data) 
		if UsuarioSerializerresponse.is_valid():
			UsuarioSerializerresponse.save()
			with open("apps/system/private_back.pem", "rb") as f:
				private_key = f.read()
			with open("apps/system/public_back.pem", "rb") as f:
				public_key = f.read()
			encoded = jwt.encode({"pas":request.data['password'] }, private_key, algorithm=settings.ALGORITM_ENCAP_BACK)

			
			self.JsonAdd(json={
				"Nombres":UsuarioSerializerresponse.data['Nombres'],
				"Apellidos":UsuarioSerializerresponse.data['Apellidos'],
				"username":UsuarioSerializerresponse.data['username'],

			})
			return Response(self.salida(), status=200)
		else:
			self.MensajeListAdd( mensaje_user = 'Ocurrio un error al procesar la solicitud', 
						mensaje_server=UsuarioSerializerresponse.errors)
			# self.JsonAdd(json=UsuarioSerializerresponse.errors)

			return Response(self.salida(), status=200)
