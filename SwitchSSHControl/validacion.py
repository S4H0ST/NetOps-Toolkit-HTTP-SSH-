import platform
import re
import subprocess
from PortControl.configuracion import ANSI

class validacion:
    def __init__(self, ip: str):
        self.ip = ip

    def checkIp(self)->bool:
        '''
        Esta funcion comprueba que la direccion IP sigue el formato correcto de una IPv4
            Args:
                self.ip (str): contiene una dirección IP

            Returns: Devuelve True si el formato de la dirección IP es valida, en caso contrario devuelve False
        '''
        # Expresión regular para verificar el formato de la dirección IP
        patron_ip = r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$'  # r = expresion literal , f = expresion especial
        if re.match(patron_ip, self.ip):  # re.match es un metodo para comparar cadenadas por patrones
            octetos = self.ip.split('.')  # divide la ip en partes individuales al encontrar "."
            for octeto in octetos:
                if not (0 <= int(octeto) <= 255):  # validar que estan en el rango de 0-255
                    return False
                return True
        else:
            return False

    # Muestra si la ip es valida o no
    def validarIp(self)->bool:
        if self.checkIp():
            print("La dirección IP es válida:", self.ip)
            return True
        else:
            print("La dirección IP proporcionada no es válida:", self.ip)
            return False
        # Comprobar que responde bien al comando PING

    def ping(self)->bool:
        '''
        Esta funcion ejecuta el comando ping a la IP añadida y mira si recibe respuesta
            Args:
                self.ip (str): contiene una dirección IP

            Returns: devuelve True si se pudo recibir respuesta, en caso contrario devuelve False
        '''
        # Define el comando de ping según el sistema operativo
        if platform.system() == 'Windows':
            command = ['ping', '-n', '1', self.ip]
        else:
            command = ['ping', '-c', '1', self.ip]
        # Ejecuta el comando de ping y captura la salida
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                packs = ANSI.color_text(f"La IP {self.ip} responde correctamente al comando PING", ANSI.YELLOW)
                print(packs)
                return True  # Devuelve True si el ping fue exitoso
        except Exception as e:
            print(f"Error al ejecutar el comando de PING: {e}")
            return False
