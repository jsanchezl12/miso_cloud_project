Descripcion del componente post-management:
- Es el microservicio permite gestionar las publicaciones. 
- Cuenta con un metodo Post que permite crear una publicación asociado al usuario al que le perenece el token.
- Solamente un usuario autorizado puede realizar esta accion por medio de un bearer token.
- Cuenta con un metodo Get que permite listar las publicaciones activos que coinciden con los parametros brindados.
- Permite consultar una publicación especifica por medio del identificador con el que se desea buscar.
- Cuenta con un metodo Get que nos permite validar la salud del servicio.