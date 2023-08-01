Descripcion del componente offer-management:
- Es el microservicio encargado de manejar las ofertas de los usuarios, crearlas y eliminarlas. 
- Cuenta con un metodo Post que en su cabezado recibe un token de autorizacion de tipo Bearer, el cual es validado por el microservicio de user-management.
- Cuenta con un metodo Get que permite listar las ofertas que coinciden con los parametros brindados.
- Permite consultar una unica oferta por medio del metodo Get con el id de la oferta deseada a buscar.
- Cuenta con un metodo Get que nos permite validar la salud del servicio.