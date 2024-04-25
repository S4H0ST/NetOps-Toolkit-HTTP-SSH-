# Scripts de ejecución remota

## execommands.py

El script verifica la disponibilidad de una dirección IP utilizando ping y realiza un reinicio (reboot) a través de SSH si la IP está activa.

Necesitas crear un archivo .env con la información necesaria para ejecutar el script:

El fichero .env tiene que seguir el siguiente formato:
```
# Archivo .env

[CONFIG]
# Configuración de redes separadas por comas
# REDES APS WIFI:
#   m: 10.xx.xx.xx/23
#   al: 10.xx.xx.xx/23
#   
redes=red1,red2,red3

# Usuario de acceso SSH
usuario=nombre_de_usuario
# Clave del usuario SSH
clave=contraseña_secreta
# Comandos a lanzar separados por comas
comandos=comando1,comando2,comando3
```
Instalamos las depedencias necesarias para el funcionamiento del script:

```
pip install -r requirements.txt
```

Para ejecutar el script utilizamos el siguiente comando:

```
python3 execommands.py --fichero path_fichero.env

```
Por defecto, tomará el fichero .env si no se especifica otro

```
python3 execommands.py

```
Y ejecutará el reinicio de acuerdo a los parámetros del .env



