from rest_framework import serializers
from apps.system.models import login

from .models import user




class UsuarioSerializer(serializers.ModelSerializer):


	class Meta:

		model = user
		fields = ('username','email', 'Nombres', 'Apellidos', 'password') 

	def __str__(self):

		return self.UsuarioSerializer

class LoginSerializer(serializers.ModelSerializer):


	class Meta:

		model = login
		fields = ('username', 'password') 

	def __str__(self):

		return self.LoginSerializer