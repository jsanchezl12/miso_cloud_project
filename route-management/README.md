Descripcion del componente route-management:
- Es el microservicio permite gestionar los trayectos que van a ser utilizados por las publicaciones. 
- Cuenta con un metodo Post que permite crear un trayecto con los datos brindados.
- Solamente un usuario autorizado puede realizar esta accion por medio de un bearer token.
- Cuenta con un metodo Get que permite listar los trayectos activos que coinciden con los parametros brindados.
- Permite consultar un trayecto especifico por medio del identificador con el que se desea buscar.
- Cuenta con un metodo Get que nos permite validar la salud del servicio.