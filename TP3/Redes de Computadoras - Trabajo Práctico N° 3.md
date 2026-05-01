# Redes de Computadoras - Trabajo Práctico N° 3
**Nombres**  
_Gianluca Ferraris; Ezequiel J. Marredo; Juan M. Painenao; Alejandro R. Stangaferro;_  
**Xi JinPING Revenge**

**Facultad de Ciencias Exactas, Físicas y Naturales**  
**Redes de Computadoras**

**Profesores**
_Facundo O. Cuneo; Santiago M. Henn;_

**30-04-2026**

---

### Información de los autores

- **Información de contacto**: _[gianlucaferraris@mi.unc.edu.ar](mailto:gianlucaferraris@mi.unc.edu.ar); [ezequiel.marredo@mi.unc.edu.ar](mailto:ezequiel.marredo@mi.unc.edu.ar); [juanpainenao@mi.unc.edu.ar](mailto:juanpainenao@mi.unc.edu.ar); [alejandro.stangaferro@mi.unc.edu.ar](mailto:alejandro.stangaferro@mi.unc.edu.ar);_

---

## Resultados

### 1) Investigación conceptual (respuestas breves). Responder en forma concisa.

#### a) ¿Qué es SSH y qué problema resuelve?

SSH (_Secure Shell_) es un protocolo de capa de aplicación que permite establecer una sesión remota cifrada sobre una red insegura, normalmente sobre TCP. Resuelve el problema de administrar equipos remotos sin exponer credenciales ni datos en texto plano, reemplazando protocolos antiguos como Telnet o rlogin que transmitían toda la información sin cifrar.

#### b) Diferencia entre autenticación y cifrado

La autenticación verifica la identidad de las partes que se comunica, mientras que el cifrado transforma los datos para que solo el destinatario legítimo pueda leerlos. Son mecanismos complementarios: SSH primero autentica al cliente y al servidor, y recién entonces cifra todo el tráfico de la sesión.

#### c) ¿Qué es una clave pública y una clave privada?

Son las dos componentes de un par de claves asimétricas. La clave pública se distribuye libremente y se usa para cifrar mensajes o verificar firmas. La clave privada permanece en poder exclusivo del dueño y se utiliza para descifrar los mensajes destinados a él o para firmar digitalmente. Lo cifrado con una solo se puede descifrar con la otra.

#### d) ¿Por qué la clave privada no debe compartirse?

Porque la clave privada es la prueba criptográfica de identidad del usuario. Quien la posea puede suplantarlo en cualquier sistema donde su clave pública esté autorizada, descifrar comunicaciones dirigidas a él y firmar en su nombre. Compartirla equivale a entregar la identidad digital completa.

#### e) ¿Qué ventajas tienen las claves SSH frente a contraseñas?

Las claves SSH son resistentes a ataques de fuerza bruta y de diccionario al tener una entropía mucho mayor que cualquier contraseña memorizable. No viajan por la red en ningún momento (la autenticación se basa en un desafío-respuesta criptográfico), permiten automatizar accesos sin almacenar contraseñas en scripts y pueden revocarse individualmente quitando la clave pública del archivo authorized_keys del servidor.

---

### 2) Conexión SSH con la VM PC1

Se estableció la conexión SSH con la VM utilizando el comando indicado en la consigna y se creó la carpeta del grupo (`XiJinping`) dentro del home del usuario remoto.

![1](https://hackmd.io/_uploads/SJf5LcapZl.png)

La imagen muestra que se accedió correctamente a la VM y se navegó al directorio creado para el grupo.

---

### 3) Captura de tráfico SSH

Se capturó el tráfico de la sesión SSH con Wireshark aplicando el filtro `ip.dst == 4.174.129.188` para aislar los paquetes dirigidos a la VM.

![2](https://hackmd.io/_uploads/ByRFUq6TWe.png)

![3](https://hackmd.io/_uploads/r1Gd8cTTbg.png)

**Análisis del paquete capturado**

Metadatos visibles (sin cifrar):
- Interfaz: `wlo1` (interfaz WiFi del cliente)
- IP origen: `172.26.92.58` (PC local)
- IP destino: `4.174.129.188` (VM)
- Puerto destino: `22` (SSH)
- Protocolo: TCP + SSH

Contenido SSH:
- Info: `Client: Encrypted packet (len=36)`
- Los bytes resaltados en azul corresponden al payload cifrado: una secuencia aparentemente aleatoria sin estructura legible.

#### ¿Podés descifrar el contenido?

No. El payload se observa como bytes sin sentido (`fb 2a 77 7c 63 cc 51 fe...`). SSH cifra todo el contenido de la sesión con algoritmos como _chacha20-poly1305_ o _aes256-gcm_ negociados durante el handshake inicial, por lo que Wireshark solo permite ver los metadatos de red (IPs, puertos, longitud del paquete) pero resulta imposible recuperar los comandos enviados o las respuestas del servidor sin las claves de sesión.

---

### 4) Servidores con netcat y captura de tráfico

#### 4.a) Servidor TCP con netcat

Se levantó un servidor TCP en la VM escuchando en el puerto 5000 con `ncat -l 5000` y se conectó la PC local con `ncat <VM_IP> 5000`. En paralelo, se ejecutó `tshark` en la VM con el filtro `port 5000` para capturar el handshake y el intercambio posterior.

![4](https://hackmd.io/_uploads/SJgCIqa6Zx.png)

En la captura se identifica el _three-way handshake_ característico de TCP (paquetes 3, 4 y 5: `SYN`, `SYN-ACK`, `ACK`) y los segmentos `[PSH, ACK]` que transportan los mensajes intercambiados.

![5](https://hackmd.io/_uploads/Sk40U96a-l.png)

Inspeccionando el contenido hexadecimal de los paquetes con `tshark -x` se observan claramente los mensajes en texto plano enviados desde la PC local (por ejemplo `djdjadlkajdlka`), confirmando que TCP **no provee cifrado**: cualquier observador en el camino puede leer el contenido íntegro.

#### 4.b) Servidor UDP con netcat


![6](https://hackmd.io/_uploads/By80UcppZl.png)

![7](https://hackmd.io/_uploads/B1_ALqp6Zl.png)

A diferencia de TCP, no existe handshake previo: el primer paquete UDP capturado ya contiene directamente el payload (`hola`, `como estas??`) en texto plano. UDP es _connectionless_ y tampoco aplica cifrado, por lo que el contenido también queda completamente expuesto.

Se repitió el ejercicio utilizando el flag `-u` de netcat para forzar el uso de UDP: `ncat -l -u 5000` en la VM y los envíos desde el cliente con `ncat -u <VM_IP> 5000`.

![8](https://hackmd.io/_uploads/BJ5AI9aTWx.png)

![9](https://hackmd.io/_uploads/S1hA8qaT-g.png)

#### 4.c) Chat entre dos VMs

Se abrieron dos sesiones SSH a VMs distintas en terminales separadas. En una de ellas se levantó un listener TCP (`ncat -l 5555`) y desde la otra se conectó con `ncat <IP_VM1> 5555`, intercambiando mensajes en formato chat.

![10](https://hackmd.io/_uploads/Sy11DqTTbx.png)

Se documenta el ida y vuelta entre ambas instancias: la VM cliente envía `hola`, la VM servidor responde `funcionó`, y luego se continúa con `hola soy vm 2`. La comunicación funciona correctamente, demostrando que netcat sirve como herramienta básica para validar conectividad y diagnóstico entre hosts en la nube.

![11](https://hackmd.io/_uploads/S1Z1v5ppZx.png)

Imagen de la conexion con ambas computadoras:
![16](https://hackmd.io/_uploads/r1Kuhq6aWl.jpg)


---

### 5) Servidor HTTP con Python

Dentro de la carpeta del grupo se creó un archivo `index.html` con un mensaje propio y se levantó un servidor HTTP simple con `python3 -m http.server 5000`.

![15](https://hackmd.io/_uploads/HJ9yP5aaWe.png)

Desde el navegador local se accedió a `http://4.174.129.188:5000` y se visualizó correctamente el comunicado servido por la VM. Los logs del servidor muestran las peticiones `GET / HTTP/1.1` con códigos `200` y `304` (este último indica que el navegador utilizó la copia en caché).

![12](https://hackmd.io/_uploads/BJXkPq66We.png)



**Captura del tráfico HTTP en Wireshark**

Filtrando con `ip.dst == 4.174.129.188` se observan los paquetes intercambiados: nuevamente aparece el handshake TCP (puerto 5000), seguido de los segmentos `[SYN]` retransmitidos y finalmente la petición `GET / HTTP/1.1` (paquete 617) sobre la cual se monta toda la respuesta del servidor.

![14-3](https://hackmd.io/_uploads/S1pIv966Zx.png)

#### ¿Pueden descifrar el contenido? ¿Podrían intervenir el contenido?

Sí, el contenido HTTP es **completamente legible**. Al inspeccionar el paquete `GET` se aprecia en texto plano la petición completa: método, ruta, encabezados (`Host`, `User-Agent`, `Accept`, etc.) y cookies. La respuesta del servidor con el HTML del comunicado también viaja sin cifrar, por lo que cualquier intermediario en el camino podría:

1. **Leer** todo lo que el cliente solicita y todo lo que el servidor responde.
2. **Modificar** el contenido en tránsito mediante un ataque _man-in-the-middle_, inyectando HTML, scripts maliciosos o redirecciones sin que el navegador del usuario lo detecte.
3. **Suplantar** al servidor presentando contenido falso, dado que HTTP no autentica al emisor.

Esta es precisamente la razón por la que HTTPS (HTTP sobre TLS) se volvió el estándar de facto en la web: añade cifrado de extremo a extremo y autenticación del servidor mediante certificados.

---

### 6) Análisis del video de Veritasium

#### a) Relación con los TPs 1, 2 y 3

El video aborda el problema de la confidencialidad y la integridad de las comunicaciones, mostrando cómo distintos mecanismos criptográficos (intercambio de claves Diffie-Hellman, cifrado simétrico y asimétrico, firmas digitales) permiten construir canales seguros sobre redes inherentemente públicas. Los conceptos vistos en los TPs anteriores se conectan directamente:

- **Modelo en capas (TP1)**: el cifrado se aplica en la capa de aplicación (HTTPS, SSH) o en una capa intermedia (TLS), sin alterar el funcionamiento de las capas inferiores. Esta independencia entre capas es la que permite proteger las comunicaciones sin rediseñar Ethernet o IP.
- **Direccionamiento y enrutamiento (TP2)**: los paquetes pasan por múltiples saltos administrados por terceros (ISPs, routers en la nube). Cada uno de estos saltos es un potencial punto de captura, lo que justifica que la seguridad no pueda confiarse al medio sino al protocolo de extremo a extremo.
- **Captura de tráfico (TP3)**: el laboratorio actual demuestra empíricamente lo que el video plantea en términos teóricos. Se observa que TCP, UDP y HTTP exponen el contenido íntegramente, mientras que SSH solo deja ver metadatos. Es exactamente la diferencia entre un canal sin protección y uno cifrado.


#### b) Confidencialidad en redes de computadoras
 
El laboratorio confirma que no se debe asumir confidencialidad por defecto en una red. Los protocolos en texto plano (HTTP, FTP, Telnet) deben considerarse comprometidos en cualquier red no controlada, por lo que el uso de protocolos cifrados (HTTPS, SSH, TLS) es una condición mínima y no un extra. Aun así, los metadatos (IPs, puertos, tamaños) siguen siendo visibles incluso con cifrado, y la gestión de claves resulta tan crítica como el cifrado en sí: una clave privada filtrada anula cualquier garantía criptográfica.
 
---
 
## Conclusiones
 
A lo largo del trabajo pudimos comprobar de forma práctica algo que veníamos viendo solo en teoría: la red, por sí misma, no garantiza ninguna confidencialidad. Capturar tráfico TCP, UDP o HTTP con Wireshark fue trivial y leer su contenido no requirió ninguna técnica sofisticada, ya que los mensajes aparecen literalmente en texto plano. En contraste, al capturar tráfico SSH solo obtuvimos metadatos y un payload ilegible, lo que ilustra de manera muy clara el efecto del cifrado.
 
La conclusión que nos llevamos es que pensar la seguridad como algo opcional o agregado a posteriori es un error: cualquier servicio expuesto debe asumir desde el primer momento que el tráfico es observable, y el uso de protocolos cifrados junto con una gestión cuidadosa de claves son la base sobre la que se construye cualquier sistema mínimamente confiable.
