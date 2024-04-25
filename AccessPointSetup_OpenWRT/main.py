from command3825 import command3825
from ejecutar import ejecutar
from conex_Ssh import conex_Ssh

"""
OBJETIVOS
- QUITAR TODA CONFIG DE SSID 
- DESPLEGAR NUEVO SSID
   + NOMBRE
   + SEGURIDAD WPA1, WPA2, WPA3
   + CANAL A RADIAR 2,4 Y 5 GHZ
   + ANCHO DE CANAL PARA 5 GHZ
   + OPCIONAL: MinRate, 802.11r, 802.11h
   + OBLIGAORIO: LIMITAR PROTOCOLO < A 802.11n
"""
def menu():
    print("---------- MENU DE CONFIGURACION ----------")
    # CONECTAR AL HOST
    conectar = conex_Ssh()
    hostname = input("Ingrese la IP del host: ")
    user = input("Ingrese el usuario: ")
    password = input("Ingrese la contraseña: ")
    ssh = conectar.connect(hostname, user, password)
    ap3825 = command3825()

    # OPCIONES
    print("\n")
    print("Elija una opcion para continuar: ")
    print("1. Quitar toda configuracion de SSID")
    print("2. Desplegar nuevo SSID")
    print("3. Salir")
    opcion = input("Ingrese una opcion: ")

    # ELECCION DE OPCION
    print("\n")
    #getguardarCambios()
    # Quitar toda configuracion de SSID
    if opcion == "1":
        print("QUITANDO TODA LA CONFIGURACION DE SSID")
        listCommands = ap3825.deleteSettings()
        # Desplegar nuevo SSID
    elif opcion == "2":
        print("DESPLIEGUE DE NUEVO SSID")
        # Comprobar si el archivo /etc/config/wireless está vacío
        bytes= ap3825.checkBytes(ssh) #guarda el valor de la salida
        print(f"el archivo tiene {bytes} bytes")
        if bytes <= '1':
            print("La carpeta /etc/config/wireless está vacía. Generando valores por defecto...")
            ap3825.defaultSettings(ssh)
        else:
            print("La carpeta /etc/config/wireless no está vacía. Continuando con la configuración...")
        ssidName = input("Ingrese el nombre del SSID: ")
        while True:
            password = input("Ingrese la contraseña del SSID: ")
            if len(password) >= 8:#validar que la contraseña tenga al menos 8 caracteres
                break
            else:
                print("La contraseña debe tener al menos 8 caracteres. Inténtalo de nuevo.")

        encryptionType = ap3825.check_typeSecurity() #obtener tipo de seguridad del SSID
        channelRadiate = ap3825.typeChannelRadiate() #obtener canal a radiar
        listCommands=ap3825.set_listCommands(ssidName, encryptionType, password, channelRadiate)
    else:
        print("Saliendo del programa...")
        exit()

    # Resumen de configuracion
    execute = ejecutar(ssh, listCommands)
    print(execute.exec())

    print("---------- Resumen de la configuración ----------")
    execute = ejecutar(ssh, ["cat /etc/config/wireless"])  # mostrar configuracion
    print(execute.exec())
    print("***************************************************")
    print("Nombre del SSID:", ssidName)
    print("La seguridad del SSID ingresada es:", encryptionType)
    print("El canal a radiar es:", channelRadiate, "Ghz")
    print("Ancho de canal para 5 Ghz:", ap3825.get_channelWidth())
    print("Cerrando sesion SSH...")
    conectar.close()  # cerramos cliente ssh


def main():
    while True:
        menu()
        # Preguntar al usuario si desea configurar otra red
        otra_red = input("¿Desea configurar otra red? (s/n): ").strip().lower()
        if otra_red != 's':
            break  # Salir del bucle si el usuario responde negativamente
    print("Saliendo del programa...")


if __name__ == "__main__":
    main()
