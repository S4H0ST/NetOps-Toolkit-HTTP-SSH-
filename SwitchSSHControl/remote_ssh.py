import paramiko
import logging
from paramiko.client import SSHClient
import validacion
from PortControl.configuracion import ANSI, configuracion

# LOGS
# Configuración del logger
logging.basicConfig(filename='../remote_execution/execommands.log',
                    level=logging.INFO,  # Puedes ajustar el nivel según tus necesidades
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Crear el objeto logger
logger = logging.getLogger(__name__)


class IpNoEncontradaError(Exception):
    def __init__(self, ip):
        self.ip = ip
        super().__init__(f"No se encontró la IP: {ip} con las claves aplicadas")


class remote_ssh:
    def __init__(self, dirIp:str, config: configuracion):
        self.dirIp = dirIp
        self.config = config
        self.check = validacion.validacion(dirIp)


#GETTER
    def get_dirIp(self):
        return self.dirIp
    def get_config(self):
        return self.config
    def get_clave(self):
        return self.config.get_clave()
    def get_usuario(self):
        return self.config.get_usuario()
    # SSH-Execute
    def sshConexion(self) -> SSHClient:  # añadir atributo comando
        '''
        Esta funcion realiza la comprobación de ping  y  la conexión ssh
        Args:
            self.dirIp (str): IP del cliente
            self.get_usuario() (str): el nombre de usuario del cliente
            self.get_clave() (str): la clave ssh del usuario al que conectarse

        Returns: devuelve un objeto de tipo cliente ssh que se usa para ejecutar comandos antes de cerrar sesion
        '''
        if self.check.ping():
            try:
                # Crea un cliente SSH
                cliente = paramiko.SSHClient()
                cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                # Conecta al host remoto
                cliente.connect(hostname=self.dirIp, username=self.get_usuario(), password=self.get_clave())
                mensaje_exitoso = f"{ANSI.GREEN}Conexión SSH exitosa.{ANSI.RESET}"
                print(mensaje_exitoso)
                logger.info("Conexion SSH exitosa.")
                # Retornamos el objeto cliente por si se quiere realizar más acciones con él
                return cliente
            except paramiko.AuthenticationException:
                mensaje_error = f"{ANSI.RED}Error de autenticación. Usuario o contraseña incorrectos.{ANSI.RESET}"
                print(mensaje_error)
                logger.error("Error de autenticacion. Usuario o contraseña incorrectos.")
            except paramiko.SSHException as e:
                mensaje_error = f"{ANSI.RED}Error al conectar por SSH: {e}{ANSI.RESET}"
                print(mensaje_error)
                logger.error(f"Error al conectar por SSH: {e}")
            except Exception as e:
                mensaje_error = f"{ANSI.RED}Error inesperado: {e}{ANSI.RESET}"
                print(mensaje_error)
                logger.error(f"Error inesperado: {e}")
                # En caso de error, retornamos None
            return None
        else:
            raise IpNoEncontradaError(ip=self.dirIp)

def cerrar_sesion_ssh(cliente:SSHClient,dirIp:str):
        # Cerrar sesión con el cliente SSH
        cliente.close()
        logger.info(f"Sesión SSH cerrada con {dirIp}.")
