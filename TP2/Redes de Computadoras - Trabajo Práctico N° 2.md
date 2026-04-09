# Redes de Computadoras - Trabajo Práctico N° 2

**Nombres**  
_Gianluca Ferraris; Ezequiel J. Marredo; Juan M. Painenao; Alejandro R. Stangaferro;_  
**Xi JinPING Revenge**

**Facultad de Ciencias Exactas, Físicas y Naturales**  
**Redes de Computadoras**
**Profesores**
_Facundo O. Cuneo; Santiago M. Henn;_
**08-04-2026**

---

### Información de los autores
 
- **Información de contacto**: _gianlucaferraris@mi.unc.edu.ar; ezequiel.marredo@mi.unc.edu.ar; juanpainenao@mi.unc.edu.ar; alejandro.stangaferro@mi.unc.edu.ar;_  

---
## Resultados

### Parte 1: Armado y verificación de cables Cat5/Cat5e bajo estándar T568A/B

#### Investigación: Pasos para Crimpar un Cable DERECHO (Norma T568B)

Para un cable derecho, ambos extremos siguen el mismo estándar. El estándar más utilizado es el T568B.

**Procedimiento de Crimpeado:**

1.  **Pelar el cable:** Quitar aproximadamente 2-3 cm de la cubierta exterior de PVC con el pelacables de la pinza crimpeadora.

2. **Desenredar y ordenar:** Separar los pares trenzados y ordenarlos según el código de colores T568B:

![H6E9bqv4IoVBwHxj3i5cExuwnhd](https://hackmd.io/_uploads/ByuiXqV3Wx.png)
*Figura 1: Esquema de color rj45 de cable directo*


3. **Aplanar y cortar:** Juntar los hilos (cables), aplanarlos y cortarlos de forma recta a unos 1.5 cm de la base del revestimiento.

4. **Insertar en el conector:** Introducir los hilos en el conector RJ-45 asegurándose de que cada uno llegue al fondo y que el orden sea correcto visto desde el frente. También se debe verificar que el revestimiento exterior entre en el conector para ser sujetado por el seguro.

5. **Crimpar:** Insertar el conector en la pinza y apretar con firmeza.

6. **Repetir el proceso para el otro extremo**
#### Construcción y Verificación

Se construyó un cable de 1.5 metros de tipo derecho.

Informe de Inspección del Cable Evaluado:

Grupo evaluado: Ethernautas V2.

![asdsadasdasd](https://hackmd.io/_uploads/SyJcMY43be.jpg)
*Figura 2: Imagen del cable del grupo a evaluar*


**Estado:** Muy bueno.

**Inspección Visual:** Se observa que los ocho cables llegan hasta el final del conector. El revestimiento amarillo del cable Cat5e no está correctamente atrapado por la cuña del conector RJ-45, no se garantiza la durabilidad, sin embargo, la funda protectora puede ayudar.

**Verificación Eléctrica:** Al conectar ambos extremos al tester de red, los LEDs del 1 al 8 se encendieron en secuencia perfecta en ambas unidades, confirmando la continuidad y el mapeo correcto para un cable derecho.

![WhatsApp Image 2026-04-08 at 11.49.52 PM](https://hackmd.io/_uploads/B14xV9Eh-e.jpg)
*Figura 3: Verificación de continuidad y mapeo de pines mediante tester digital*

### Parte 2: Equipamiento Físico y Configuración

# Parte 2: Equipamiento físico, verificación y utilización de equipos de red y análisis de tráfico

## 1) Características principales del switch utilizado

Al no poder realizar la conexión de consola con el switch Cisco Catalyst 2950 Series, se utilizó otro switch disponible en el aula, el TP-Link TL-SF1008D, un switch no administrable de 8 puertos.

![100031251](https://hackmd.io/_uploads/rkbBH5V3Wx.jpg)
*Figura 4: Switch utilizado para el trabajo*


### Switch TP-Link TL-SF1008D

| Característica | Detalle |
|---|---|
| Tipo de dispositivo | Switch no administrable (unmanaged), orientado a entornos SOHO |
| Interfaces | 8 puertos RJ45 10/100 Mbps con Auto-Negociación y Auto-MDI/MDIX (elimina la necesidad de cables crossover) |
| Capacidad de conmutación | 1.6 Gbps (arquitectura non-blocking, conmutación a velocidad de línea completa) |
| Tabla de direcciones MAC | Hasta 1000 entradas |
| Velocidad por puerto | 10/100 Mbps en Half Duplex; hasta 200 Mbps en Full Duplex |
| Método de reenvío | Store-and-Forward |
| Control de flujo | IEEE 802.3x en Full Duplex / Back-Pressure en Half Duplex |
| Estándares soportados | IEEE 802.3 (Ethernet), IEEE 802.3u (Fast Ethernet), IEEE 802.3x (Flow Control) |
| Consumo máximo | 2.05 W (220V/50Hz), con tecnología Green Ethernet que reduce hasta un 60% el consumo ajustando según estado del enlace y longitud del cable |
| Dimensiones | 134.5 × 79 × 22.5 mm, diseño compacto de escritorio, sin ventilador (fanless) |
| Instalación | Plug and Play, sin configuración requerida |

---

## 2) Checklists de procedimientos

Esta parte en la práctica no se realizó, debido a que se utilizó otro switch. Sin embargo, se agregó en el informe para tener una noción de como seria el proceso.

### a) Conexión de una PC al puerto de consola del switch Cisco a 9600 baudios con PuTTY

1. Conectar el cable serie al extremo RJ-45 del cable de consola del switch.
2. Si la PC no posee puerto serie, utilizar un adaptador USB-Serie y conectarlo a un puerto USB de la PC.
3. Verificar en el sistema operativo qué puerto COM fue asignado al adaptador.
4. Abrir PuTTY y configurar la conexión.
5. Hacer clic en Open. Si la conexión es exitosa, se accede a la CLI del switch.
6. Turnarse entre los integrantes del grupo para verificar el acceso a la consola.

### b) Acceso a las opciones de administración del switch y modificación de claves

1. Desde la consola del switch, acceder al modo User EXEC.
2. Ingresar al modo privilegiado.
3. Ingresar al modo de configuración global.
4. Configurar contraseña de consola:
   ```
   line console 0
   password <nueva_contraseña>
   login
   exit
   ```
5. Configurar contraseña de modo privilegiado (enable):
   ```
   enable secret <nueva_contraseña>
   ```
6. Guardar la configuración: `write memory` o `copy running-config startup-config`.

### c) Conectar computadoras al switch, configurar una red y testear conectividad

1. Conectar cada computadora a un puerto del switch utilizando cables Ethernet.
2. Verificar las interfaces de red disponibles en cada PC.
4. Asignar una dirección IP manualmente, ya que no hay servidor DHCP en la red.
5. Verificar que la configuración se aplicó correctamente repitiendo los comandos del paso 2.
6. Realizar las pruebas de conectividad:
   - `ping <ip_propia>` (prueba de loopback sobre la interfaz).
   - `ping <ip_compañero>` (prueba de conectividad con la otra PC a través del switch).

---

## 3) Prueba de conectividad entre grupos

Se conectó una computadora de cada grupo al switch TP-Link utilizando los cables armados en la Parte 1 del TP.

### Configuración utilizada

Se asignaron direcciones IP en el rango `192.168.x.x` y se configuró la otra PC para estar en el mismo segmento de red.

### Resultado del ping

![image](https://hackmd.io/_uploads/BJiSd5NhZg.png)


## Conclusiones
Este trabajo práctico permitió integrar de forma práctica los conceptos de las capas física y de enlace de datos: desde el armado y verificación de cables Ethernet hasta su uso real para establecer comunicación entre PCs a través de un switch. 
Si bien no se pudo acceder al switch administrable Cisco por falta de adaptadores, el uso del TP-Link TL-SF1008D permitió cumplir el objetivo central de verificar conectividad en una LAN. El inconveniente con la asignación de IPs y su resolución mediante APIPA reforzó la importancia de comprender los mecanismos de direccionamiento para lograr comunicación efectiva entre dispositivos.
