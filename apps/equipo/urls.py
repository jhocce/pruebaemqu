from django.urls import path
from .views import EquipoAPI, TestAPI, TesttestAPI



urlpatterns = [
	path('', EquipoAPI.as_view(), name="equipo"),
	path('test/', TestAPI.as_view(), name="test"),
	path('make/test/', TesttestAPI.as_view(), name="hacertest"),
	# path('login/', LoginUserAPI.as_view(), name="login"),
    # path('logout/', LogoutUserApi.as_view(), name="logout"),	

	# path('logout/', LogoutUserApi.as_view(), name="logout"),	
	# path('detallestoken/', DetallesToken.as_view(), name="DetallesToken"),	
]