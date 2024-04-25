import argparse
import configparser


class configuracion():
    def __init__(self, usuario: str, clave: str):
        self.user = usuario
        self.password = clave

    # comandos: list
    def get_usuario(self):
        return self.user

    def get_clave(self):
        return self.password

    def __str__(self):
        return f"Usuario: {self.user}, Contraseña: {self.password}"


def read_config(path: str) -> configuracion:
    '''
    Esta funcion lee un fichero .env y saca los valores de usuario y clave SSH
        Args:
            path (str): contiene el path del archivo .env

        Returns: devuelve un objeto configuracion que contiene el usuario y la clave SSH
    '''
    config = configparser.ConfigParser()
    config.read(path)
    result = ANSI.color_text("##### Datos del archivo de configuración #####", ANSI.PURPLE)
    print(result)
    usuario = config["CONFIG"]["usuario"]
    clave = config["CONFIG"]["clave"]
    # print("Usuario: ", usuario,"\nClave: ", clave)
    return configuracion(usuario, clave)


def crear_parser() -> configuracion:
    '''
    Esta funcion crea un parser que es un componente para analizar datos de un formato especifico en este caso se especifica que será .env
        Args:
            path (str): contiene el path del archivo .env

        Returns: devuelve un objeto configuracion que contiene el usuario y la clave SSH
    '''
    parser = argparse.ArgumentParser(
        description='''
            Los campos a insertar son -f [NOMBRE FICHERO] . Indica el fichero que tiene los datos, tendra formato \n[CONFIG]\nred=...\nusuario=...\nclave=...\ncomandos=...
            Para la red puedes especificar varios direccionamientos separados por comas, para varios comandos igual''',
        epilog="""""")
    parser.add_argument('--fichero', '-f', default='.env', action='store',
                        dest='fichero', help='Nombre del fichero que vamos a escribir', type=str)
    args = parser.parse_args()
    if not args.fichero.endswith('.env'):
        parser.error("El archivo de configuración debe tener la extensión .env")
    config = read_config(args.fichero)
    return config


class ANSI:
    GREEN = "\033[92m"
    RED = "\033[91m"
    ORANGE = "\033[93m"
    BLUE = "\033[94m"
    BROWN = "\033[33m"
    YELLOW = "\033[33m"
    PURPLE = "\033[95m"
    RESET = "\033[0m"

    @staticmethod
    def color_text(text, color_code)->str:
        return color_code + text + ANSI.RESET
