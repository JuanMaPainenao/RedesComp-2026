# Redes de Computadoras - Trabajo Práctico N° 1

**Nombres**  
_Gianluca Ferraris; Ezequiel J. Marredo; Juan M. Painenao; Alejandro R. Stangaferro;_  
**Xi JinPING Revenge**

**Facultad de Ciencias Exactas, Físicas y Naturales**  
**Comunicaciones de Datos**
**Profesores**
_Facundo O. Cuneo; Santiago M. Henn;_
**26-03-2026**

---

### Información de los autores
 
- **Información de contacto**: _gianlucaferraris@mi.unc.edu.ar; ezequiel.marredo@mi.unc.edu.ar; juanpainenao@mi.unc.edu.ar; alejandro.stangaferro@mi.unc.edu.ar;_  

---
## Resultados

### Parte 1. Repaso general didáctico: Simulación de envío de paquetes, ARP y ruteo entre redes.

1) Identificación de los dispositivos y armado de la topología:
Nuestro grupo trabajo como uno de los tres routers, así mismo estábamos conectados a los otros 2 routers y además teníamos 3 hosts, cada host conformado por un grupo donde uno de los integrantes actuaba como gateway.

Información de red:
| Campo               | Valor          |
|---------------------|----------------|
| **Dispositivo**     | Router 1       |
| **Rol**             | ROUTER         |
| **MAC**             | AA:43:80       |
| **Redes conectadas**| 10.13.0.0/24, 10.6.0.0/24, 10.12.0.0/24 |
| **Gateway**         | No aplica      |

2) Armado de topología

![TP1](https://hackmd.io/_uploads/Hk3Y_z7j-e.png)


Tabla de routeo:

| Red Destino     | Next Hop              |
|-----------------|-----------------------|
| 10.13.0.0/24    | Conexión directa |
| 10.6.0.0/24     | Conexión directa |
| 10.12.0.0/24    | Conexión directa |
| 10.19.0.0/24    | Router 2 (AA:45:92)   |
| 10.9.0.0/24     | Router 2 (AA:45:92)   |
| 10.11.0.0/24    | Router 2 (AA:45:92)   |
| 10.16.0.0/24    | Router 3 (AC:45:70)   |
| 10.10.0.0/24    | Router 3 (AC:45:70)   |
| 10.5.0.0/24     | Router 3 (AC:45:70)   |
    
    
3)
Nuestro grupo representaba al Router 1 (MAC: AA:43:80), por lo que no generábamos paquetes propios como los hosts. Nuestra función era recibir, procesar y reenviar los paquetes que circulaban por la red.

Al ser un router, no conformábamos paquetes con payload propia. Los hosts de nuestras LANs (10.13.0.0/24, 10.6.0.0/24 y 10.12.0.0/24) o los otros routers nos enviaban frames Ethernet dirigidos a nuestra MAC (AA:43:80), conteniendo paquetes IP con destino a otras redes.

Nuestro trabajo consistía en reencapsular el paquete IP en un nuevo frame Ethernet con las MACs correspondientes al siguiente salto, sin modificar la IP de origen ni la IP de destino del paquete, las MACs podían ser al host final o a otro router intermedio.

4) Es la actividad en si realizada en clase.

5) 
A) 
La IP de destino del paquete se mantuvo constante mientras que la MAC de destino cambia en cada salto debido a que cada una opera en una capa diferente del modelo de red. La dirección IP es una dirección lógica que identifica al emisor y receptor final en la comunicación, mientras que la dirección MAC es una dirección física que solo tiene alcance local, solo es válida dentro de un mismo segmento de red.

B)
El host envía el paquete al default gateway en lugar de buscarlo directamente ya que el host no lo puede alcanzar por si solo. Ya que el protocolo ARP funciona únicamente dentro de la misma LAN. El gateway si tiene conexión con otras redes y posee una tabla de routeo que le permite determinar a donde enviar el paquete.

C) 
El modelo de ruteo hop-by-hop se basa en que cada router toma decisiones de forma independiente y local, basándose solamente en su tabla de routeo. Las ventajas que esta manera de trabajar ofrece son:
- Escalabilidad: Cada router solo necesita saber a quién entregarle el paquete como siguiente paso, no la ruta completa. Lo que permite la escalabilidad ya que ningún dispositivo tiene que tener un mapa global.
- Adaptabilidad: Si un enlace se cae o un router deja de funcionar, los routers vecinos pueden actualizar sus tablas de routeo y encontrar caminos alternativos.
- Simplicidad: Simple, ya que cada router solo debe mirar la IP de destino y consultar con su tabla de routeo y reenviar. No necesita coordinar con ningún router para tomar una decisión.
- Descentralización: No existe punto central que decida la ruta de todos los paquetes.

D)
Es necesario reconstruir el frame Ethernet en cada salto ya que las direcciones MACs van variando. Cuando un router recibe un frame, las MACs que recibe corresponden al enlace por el que llego, para reenviarlo por otro enlace hay que actualizar la MAC de origen, que es la MAC del propio router y la MAC de destino que es la del siguiente dispositivo en el camino.

E) 
El campo TTL previene el problema de los loops de ruteo. Los loops de ruteo ocurren cuando por error en las tablas de routeo, dos o más router se reenvían un paquete indefinidamente. 
TTL se utiliza para que cada vez que un router procesa un paquete, decrementa el TTL en 1. Cuando el TTL llega a 0, el router descarta el paquete en lugar de reenviarlo. De esta forma se garantiza que todo paquete tenga un numero máximo de saltos que puede dar antes de que sea eliminado.

### Parte 2. Inyección y detección de errores.

En esta actividad de laboratorio, a nuestro grupo le correspondió el rol de Host. Como método de detección de errores (EDAC), se estableció por consigna el uso de paridad par, tanto para el envío como para la recepción de datos. La actividad fue llevada a cabo mediante papeles con los datos escritos.

Para la etapa de transmisión, se nos asignó un payload que codificamos según el método indicado y lo enviamos a una IP elegida por nosotros. Por otro lado, para la etapa de recepción, debíamos analizar la integridad de los paquetes recibidos y completar una tabla de documentación.

Recibimos un paquete proveniente de la `IP 10.1.0.1` con el siguiente payload en formato hexadecimal: `4260h` (`0100 0010 0110 0000`) y un código de EDAC = `0011`. Al analizar el paquete bajo el criterio de EDAC dado, determinamos que el EDAC debería haber sido `0011` (un bit por cada nible, contando la cantidad de unos):
* 0100 -> impar = 1
* 0010 -> impar = 1
* 0110 -> par = 0
* 0000 -> par = 0

**Resultado esperado paridad par: 1100**

Como el EDAC recibido no coincide con el calculado, planteamos las siguientes hipótesis:
1. Se alteraron varios bits del payload o del propio código EDAC provocando discrepancia.
2. El grupo emisor utilizó paridad impar en lugar de paridad par. Si se aplica paridad impar al payload `4260h`, el código resultante es efectivamente `0011`, lo que explicaría la coincidencia y por qué el EDAC recibido está invertido al calculado al nuestro.
3. El grupo emisor cometió un error al transcribir o calcular el código EDAC.

En conclusión, aunque no se puede determinar con total certeza si el paquete fue modificado intencionalmente en el trayecto, objetivamente el paquete recibido no es íntegro bajo los parámetros de paridad par establecidos para la práctica.
