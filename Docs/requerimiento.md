# Desarrollo #

La empresa Rios del desierto SAS, necesita implementar para el equipo de SAC una herramienta que le permita consultar la información de un cliente ingresando únicamente su número de documento. Esto con el fin de minimizar tiempos en las llamadas de soporte. Además, desea fidelizar a sus mejores clientes.

*** Requerimiento del cliente: ***

1. Crear una página web que tenga un modelo con los datos básicos del cliente (Tipo de documento, Numero de documento, Nombre, Apellido, Correo, Telefono y los que vean necesarios) y otro modelo con las compras asociadas a cada cliente (añadir los campos que consideren, sobre todo teniendo en cuenta el punto 5.).

2. Ya en el Frontend de la página se debe crear un formulario con los campos:
a. Tipo de documento (NIT, Cedula, Pasaporte)
b. Numero de documento.
c. Botón buscar.

3. Desarrollar una API que consulte por número de documento la información del cliente en una tabla. (La tabla debe estar en SQL Lite) y debe tener los campos:
a. Numero de documento
b. Nombre
c. Apellido
d. Correo
e. Teléfono

4. El resultado de la consulta se debe mostrar en pantalla la información del cliente y tener la opción de exportarla (Puede ser en formato .csv, Excel o txt).

5. Finalmente, la empresa desea fidelizar a los clientes con mayor número de compras, por lo tanto, se debe crear un reporte en Excel con los datos básicos del cliente y el monto total de las compras del cliente en el último mes, la empresa solo considerará fidelizar a los clientes que superen un monto de compras de 5’000.000 de pesos COP.

Este desarrollo debe ser realizado en Python para el Backend, y el frontend deberá ser realizado con React. Las peticiones se deben hacer vía API.

*** Entregables: ***
1. Guía de Implementación (Paso a paso de como colocarlo en ambiente productivo)
2. Paquetes de Instalación (Preferiblemente en GIT)
3. Documentación técnica (Básica)
4. La base de datos implementada.

*** Consideraciones: ***
1. Se recomienda el uso de django o flask para el backend de la página.
2. Para la automatización se deben tener suficientes datos para traer por lo menos un cliente que cumpla las condiciones dadas.
3. Usar el ORM de django o flask suma más puntos que crear toda la base de datos de cero.
4. Usar pandas para la automatización igualmente suma puntos.
5. Tenga en cuenta que puede que solo 2 tablas (Usuarios y compras) no es suficiente, por lo que se le evaluará mejor si tiene un modelado de datos más elaborado, como por ejemplo añadir una tabla de tipos de documentos, etc.