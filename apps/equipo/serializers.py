from .models import Equipo, Test
from rest_framework import serializers


class TestSerializer(serializers.ModelSerializer):


	class Meta:

		model = Test
		fields = ("Creado","responde","enviados", "recibidos", "perdidos", "maximo", "media", "minimo") 

	def __str__(self):

		return self.TestSerializer


class EquipoSerializer(serializers.ModelSerializer):

	# test = TestSerializer()
	test = TestSerializer(
        many=True,
        read_only=True

    )
	class Meta:

		model = Equipo
		fields = ("pk_publica","Nombre", "direccion", "paquetes", "test") 

	def __str__(self):

		return self.EquipoSerializer

class EquipoSerializer2(serializers.ModelSerializer):


	class Meta:

		model = Equipo
		fields = ("pk_publica","Nombre", "direccion", "paquetes") 

	def __str__(self):

		return self.EquipoSerializer2
	