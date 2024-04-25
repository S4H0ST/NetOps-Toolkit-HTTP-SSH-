Script para ejecutar comandos por SSH
-
____
Para ejecutar el script:
```
py script.py -f <fichero.env>
```
El fichero ```.env```deberá de seguir el siguiente formato para que se pueda leer correctamente y leer el usuario y clave del cliente ssh al que se quiere conectar.
```
[CONFIG]
# Usuario de acceso SSH
usuario=user 
# Clave del usuario SSH
clave=password 
```
Se remplaza ```user```, por el nombre de usuario del cliente ssh (sin comillas), y se remplaza ```password``` por la clave del cliente ssh (sin comillas).
Se mantiene ```[CONFIG]  usuario=  clave=``` 

**Instalar requirement.txt**
-
____
1. Desde la terminal o línea de comandos nos dirigimos a la ubicación donde se encuentra el archivo.
```
cd scripts_varios/Puertos/
```
2. Ejecutamos `pip install -r requirements.txt`. Esto instalará todos los paquetes listados en el archivo `requirements.txt`
```
pip install -r requirements.txt
```
---
**Resumen del contenido de las clases**
-
____
- configuracion
```
__init__(self, usuario:str, clave:str)
get_usuario(self)
get_clave(self)
read_config(path: str) -> configuracion
crear_parser() -> configuracion
class ANSI
    color_text(text, color_code)->str
```
- remote_ssh
```
class IpNoEncontradaError(Exception)
__init__(self, dirIp:str, config: configuracion)
get_dirIp()->str:
get_config()->configuracion:
get_clave()->str:
get_usuario()->str:
sshConexion() -> SSHClient
cerrar_sesion_ssh(cliente:SSHClient,dirIp:str)
```
- exe_commands
```
__init__(self, sshObj: remote_ssh, commands: list[str])
ejecutar(self)->str
get_cliente_info(self)
```
- validacion
```
__init__(self, ip: str)
checkIp(self.ip:str)->bool
validarIp(self.ip:str)->bool
ping(self.ip:str)->bool
```
- scripts
```
Programa principal
```