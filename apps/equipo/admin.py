from django.contrib import admin
from .models import Equipo, Test
# Register your models here.

class EquipoAdmin(admin.ModelAdmin):
    list_display = ('Nombre', 'direccion', 'servicio')

admin.site.register(Equipo, EquipoAdmin)

# admin.site.register(Equipo)


class TestAdmin(admin.ModelAdmin):
    list_display = ("equipo","responde", "enviados", "recibidos", "perdidos", "maximo", "media", "minimo")
admin.site.register(Test, TestAdmin)
