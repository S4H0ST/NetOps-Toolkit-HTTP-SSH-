import logging
from PortControl.configuracion import ANSI
import remote_ssh

# Configuración del logger
logging.basicConfig(filename='../remote_execution/execommands.log',
                    level=logging.INFO,  # Puedes ajustar el nivel según tus necesidades
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Crear el objeto logger
logger = logging.getLogger(__name__)


class exe_commands:
    def __init__(self, sshObj: remote_ssh, commands: list[str]):
        self.commands = commands
        self.cliente_info = sshObj
        self.cliente_ssh = sshObj.sshConexion()

    def ejecutar(self)->str:
        '''
        Esta funcion ejecuta los comandos para modificar los puertos especificos
            Args:
                  self.cliente_info (remote_ssh): contiene el usuario, clave y la IP a las que se van a conectar
                  self.cliente_ssh (SSHClient): contiene una conexión abierta de ssh con la información de self.cliente_info
                  self.commands (list[str]): lista de comandos
            Returns: devuelve una cadena concatenada con un resumen las acciones realizadas a una ip determinada
        '''
        salida = ""
        for comando in self.commands:
            ipTmp = self.cliente_info.get_dirIp()
            stdin, stdout, stderr = self.cliente_ssh.exec_command(comando)
            output = stdout.read().decode('utf-8')  # lectura del comando
            mensaje = "IP=" + ipTmp + ";COMANDO=" + str(comando) + "\n"
            salida += mensaje
            logger.info(f"Se ha ejecutado el comando {comando} en {ipTmp}.")
            print(ANSI.color_text(f"Se ha ejecutado el comando {comando} en {ipTmp}.", ANSI.BLUE))
            print(output)  # imprimir resultado del comando introducido
        remote_ssh.cerrar_sesion_ssh(cliente=self.cliente_ssh, dirIp =self.get_cliente_info().get_dirIp())  # cerramos sesion ssh
        return salida  # salida concatenada por eso se muestra un resumen

    # GETTER
    def get_cliente_info(self)->remote_ssh:
        return self.cliente_info
