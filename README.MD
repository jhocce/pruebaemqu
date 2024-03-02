
## Sobre la instalación: 
* * *
Requisitos:
1. Tener instalado GIT.
2. Python versión 3.6, >.
3. Un entorno virtual listo para usar.


## Nota 

* La Bd usada para esta prueba fue "sqlite3" por lo que no requiere de mas configuracion.
* Recordar instalar los requerimientos.
* Ya la configuración esta indicada para que inicie en un entorno local por lo que no es necesario señalar un archivo de configuracion al iniciar
	(myenv)  C://<ruta>/university > python manage.py runserver 

## Inicialización 

* No es necesario pero si se desea el flujo de creacion de super usuario desde la consola con el comando CREATESUPERUSER esta controlado:
	(myenv)  C://<ruta>/university > python manage.py createsuperuser 
	si bien la estructura de archivos contempla un archivo configuracion local y es posible colocar otro para deploy, para este escenario solo se contempla el uso local del proyecto por lo que no se tratara todos los aspectos como un trabajo local.

* Entrar al servidor local http://localhost:8000/api/user/registrar y proceder al registro de un usuario.
* Para hacer login desde el api http://localhost:8000/api/user/login/
* Si se desea entrar al panel administrador se puede hacer el admin de django http://localhost:8000/admin/ 
* Solo estos Endpoint señalados aca no contienen validacion de usuario a traves de token por lo que tambien podra ver los templates por default de DRF y consumirlos desde una pestaña de navegador.
* Nota aclaratoria: solo el super usuario generado desde consola puede acceder al panel administrativo lo usuarios generados en el api solo tendran acceso a las funcionalidades del api.
* Toda la documentacion necesaria para consumir el api se encuentra en el carpeta postman, la cual contiene la informacion necesaria acerca del funcionamiento de la misma, por favor prestar atencion en los comentarios/documentacion al borde de los request en las colecciones.
* Tambien se cuenta con documentacion swagger y redoc en http://localhost:8000/swagger/ y http://localhost:8000/redoc/ respectivamente pero por falta de tiempo no se logro trabajar de manera correcta.

## Aspectos tecnicos
*  Para que el servicio funcione de manera correcta se recomienda hacer uso de SO windows con configuracion de lenguaje en español en cualquiera de sus variantes, el codigo en un principio deberia funcionar en en sistemas linux pero no se logro completar un ciclo de pruebas en la maquina virtual.