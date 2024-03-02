from django import forms
from django.contrib.auth.hashers import make_password

from .models import user

class DatosUsuarioForm(forms.ModelForm):

	# def __init__(self, *args, **kwargs):
		
	# 	super(self.__class__, self).__init__(*args, **kwargs)		
	# 	self.fields['configuracion'].required = False


	class Meta:
		model = user
		fields = [
					
					'password', 
					'Nombres',
					'Apellidos',
					'email'
					]

		widgets = {
			
			'email':forms.TextInput(attrs ={ 'class':"form-control", 'title':'Puedes usar lo que sea siempre que tenga un maximo de 50 caracteres.'}),
			'password':forms.PasswordInput(attrs ={ 'class':"form-control", 'title':'Tu Contraseña'}),
			'Nombres':forms.TextInput(attrs ={ 'class':"form-control",'title':"Nombres "}),
			'Apellidos':forms.TextInput(attrs ={ 'class':"form-control", 'title':'Apellidos'}),
		}

	def clean_password(self):
		password = self.cleaned_data['password']
		return make_password(password)
