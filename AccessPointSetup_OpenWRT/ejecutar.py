import logging

from netmiko import ConnectHandler



logging.basicConfig(filename='./execommands.log',
                    level=logging.INFO,  # Puedes ajustar el nivel según tus necesidades
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Crear el objeto logger
logger = logging.getLogger(__name__)


class ejecutar():
    def __init__(self, cliente: ConnectHandler, commands: list[str]):
        '''
        Este constructor de inicialización para la ejecucion de comandos remotos
        :param cliente(ConnectHandler): cliente SSH
        :param commands(list[str]): lista de comandos a ejecutar
        '''
        self.cliente_ssh = cliente
        self.commands = commands

    def exec(self) -> str:
        '''
        Esta función se encarga de ejecutar comandos en un host remoto
        :return(str): salida de los comandos ejecutados
        '''
        salida = ""
        for comando in self.commands:
            ipTmp = self.cliente_ssh.find_prompt()  # Get the current device prompt
            output = self.cliente_ssh.send_command(comando)  # Send the command
            if output is None:
                # Manejar el caso en el que la salida es None
                print("La salida de la función es None.")
            else:
                # Continuar con el procesamiento normal
                output = output.rstrip()  # Eliminar espacios en blanco al final de la cadena
            mensaje = "IP=" + ipTmp + ";COMANDO=" + str(comando) + "\n"
            salida += mensaje
            logger.info(f"Se ha ejecutado el comando {comando} en {ipTmp}.")
              # imprimir resultado del comando introducido
        return output


