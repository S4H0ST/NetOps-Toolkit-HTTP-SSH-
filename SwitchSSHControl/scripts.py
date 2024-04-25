# Importar los módulos necesarios
from PortControl import configuracion, exe_commands, remote_ssh
from PortControl.configuracion import ANSI
import validacion

Redes = []
# Menu del script
colorMenu = ANSI.color_text("########################\n    MENU PRINCIPAL\n########################", ANSI.PURPLE)
introIp = ANSI.color_text("Introduce una IP (o 'q' para terminar): ", ANSI.BROWN)
execCom = ANSI.color_text("Introduce el comando a ejecutar: ", ANSI.BROWN)
lista_Redes = []
print(colorMenu);
while True:
    while True:
        red_Ip = input(introIp)
        checkFormato= validacion.validacion(red_Ip)
        if red_Ip.lower() == 'q':
            break
        if checkFormato.validarIp():
            break
    if red_Ip.lower() == 'q':
        break

    lista_comandos = []
    while True:
        lista_comandos.append(input(execCom))
        continuar = input("¿Deseas añadir más comandos? (s/n): ")
        if continuar.lower() != 's':
            args = configuracion.crear_parser()
            newRed = remote_ssh.remote_ssh(red_Ip, args) #newRed = remote_ssh(ip,config)
            lista_Redes.append(exe_commands.exe_commands(newRed, lista_comandos)) #lista_Redes = exe_commands(remote_ssh,lista[str])
            break

#RESULTADO DE LOS DATOS INTRODUCIDOS
    content= ANSI.color_text("Dirección IP:",ANSI.ORANGE)
for red in lista_Redes:
    print(f"{content} {red.get_cliente_info().get_dirIp()}")
    red.ejecutar()

