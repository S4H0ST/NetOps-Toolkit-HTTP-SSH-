import logging
import os
import platform
from netmiko import ConnectHandler


# LOGS
# Configuración del logger
logging.basicConfig(filename='./execommands.log',
                    level=logging.INFO,  # Puedes ajustar el nivel según tus necesidades
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Crear el objeto logger
logger = logging.getLogger(__name__)


class conex_Ssh:
    def __init__(self):
        self.client = None

    def connect(self, hostname: str, username: str, password: str)-> ConnectHandler:
        '''
        Esta función se encarga de establecer una conexión SSH con un host remoto
        :param hostname(str): dirección IP del host
        :param username(str): nombre de usuario
        :param password(str): contraseña del usuario
        :return(ConnectHandler): cliente SSH
        '''
        # Verificar si el host es accesible
        if platform.system() == "Windows":
            response = os.system(f"ping -n 1 {hostname} > nul 2>&1")
        else:
            response = os.system(f"ping -c 1 {hostname} > /dev/null 2>&1")

        if response == 0:
            try:
                self.client = ConnectHandler(device_type='linux', ip=hostname, username=username, password=password)
                print(f"Conexion existosa con {"10.103.82.78"}")
                logger.info(f"Successfully connected to {"10.103.82.78"}")
                return self.client
            except Exception as e:
                print(f"Autenticación fallida para {hostname} con usuario {username}")
                logger.error(f"Authentication failed for {hostname} with user {username}")
                exit()
        else:
            print(f"No existe {hostname}")
            logger.error(f"Cannot connect to {"10.103.82.78"}: Host is not reachable")
        return None

    def close(self):
        self.client.disconnect()
        logger.info("SSH connection closed")

# GETTER
