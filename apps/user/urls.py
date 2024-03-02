from django.urls import path
from .views import registro, login1, LoginUserAPI, LogoutUserApi, RegisterApi



urlpatterns = [
	path('registrar', RegisterApi.as_view(), name="registroapi"),
	path('login/', LoginUserAPI.as_view(), name="login"),
    path('logout/', LogoutUserApi.as_view(), name="logout"),	

	# path('logout/', LogoutUserApi.as_view(), name="logout"),	
	# path('detallestoken/', DetallesToken.as_view(), name="DetallesToken"),	
]