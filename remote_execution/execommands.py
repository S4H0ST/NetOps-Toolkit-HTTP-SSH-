# Importar los módulos necesarios
import argparse
import configparser
import logging
import os
import platform
import sys
import threading
import paramiko
import ipcalc
import art
from pydantic import BaseModel
#Colores
class ANSI():
    def background(code):
        return "\33[{code}m".format(code=code)
  
    def style_text(code):
        return "\33[{code}m".format(code=code)
  
    def color_text(code):
        return "\33[{code}m".format(code=code)

titulo = "REMOTE_EXECUTION"
version = "Version_1.0"
ascii_art_titulo = art.text2art(titulo)  # Genera arte ASCII



#LOGS
# Configuración del logger
logging.basicConfig(filename='execommands.log',
                    level=logging.WARNING,  # Puedes ajustar el nivel según tus necesidades
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Crear el objeto logger
logger = logging.getLogger(__name__)



class configuracion(BaseModel):
    redes: list
    usuario: str
    clave: str
    comandos: list

#Mira a ver si está activo y realiza un reboot
def ping_and_execute(ip:str,usuario:str,clave:str,comandos:list):
    if platform.system() == 'Windows':
        resultado = os.system("ping -n 1 " + str(ip) + " >nul 2>&1")
    else:
        resultado = os.system("ping -c 1 " + str(ip) + " > /dev/null 2>&1")
    if resultado == 0:
        logger.info(ANSI.color_text(32)+"PING OK " + str(ip))
        try:
            cliente = paramiko.SSHClient()
            cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            cliente.connect(str(ip), username=usuario, password=clave)
            for comando in comandos:
                stdin, stdout, stderr = cliente.exec_command(comando)
                #Agrupar esto en una funcion  para logear y printear
                logger.info(f"Se ha ejecutado el comando {comando} en {ip}.")
                print(ANSI.color_text(32)+f"Se ha ejecutado el comando {comando} en {ip}.")
            cliente.close()
        except Exception as e:
            logger.warning(f"No se ha podido conectar por SSH a {ip}. Error: {e}")
            print(ANSI.color_text(31)+f"No se ha podido conectar por SSH a {ip}. Error: {e}")
    else:
        logger.warning(f"La IP {ip} no responde al ping")
        print( ANSI.color_text(31)+f"La IP {ip} no responde al ping")

#Lee la configuración del fichero especificado.
def read_config(path:str)->configuracion:
    config = configparser.ConfigParser()
    config.read(path)
    return configuracion(redes=config["CONFIG"]["redes"].split(','),usuario=config["CONFIG"]["usuario"],clave=config["CONFIG"]["clave"],comandos=config["CONFIG"]["comandos"].split(','))



if __name__ == "__main__":

    print( ANSI.background(1) + ANSI.color_text(94) + ANSI.style_text(5) +ascii_art_titulo)
    print(version)
    print(ANSI.background(0) + ANSI.color_text(39) + ANSI.style_text(1))
    


    parser = argparse.ArgumentParser(
        description='''
        Los campos a insertar son -f [NOMBRE FICHERO] . Indica el fichero que tiene los datos, tendra formato \n[CONFIG]\nred=...\nusuario=...\nclave=...\ncomandos=...
        Para la red puedes especificar varios direccionamientos separados por comas, para varios comandos igual''',
        epilog="""""")
    
    #parser.print_help()

    parser.add_argument('--fichero', '-f', default='.env', action='store',
                        dest='fichero', help='Nombre del fichero que vamos a escribir', type=str)

    args = parser.parse_args()

    # Definir la red y las credenciales
    config = read_config(args.fichero)
    
    # Crear una lista de direcciones IP dentro de la red
    ips=[]
    for red in config.redes:
        ips += ipcalc.Network(red)
        

    #Creamos un thread por cada host
    threads = []
    for host in ips:
        thread = threading.Thread(target=ping_and_execute, args=(host,config.usuario,config.clave,config.comandos))
        threads.append(thread)
        thread.start()

    # Esperar a que todos los threads hayan terminado
    for thread in threads:
        thread.join()

    print(ANSI.background(0) + ANSI.color_text(39) + ANSI.style_text(1))