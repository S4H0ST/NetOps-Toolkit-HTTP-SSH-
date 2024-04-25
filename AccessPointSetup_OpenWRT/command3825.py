from netmiko import ConnectHandler

from ejecutar import ejecutar


class command3825:
    def __init__(self):
        self.keepChanges = ["uci commit wireless", "wifi reload", "/etc/init.d/network restart"]
        self.deleteConfig = ["uci delete wireless.radio0", "uci delete wireless.default_radio0",
                             "uci delete wireless.radio1", "uci delete wireless.default_radio1", "uci commit wireless"]
        self.channelWidth = None
        self.ssidName = None
        self.typeSecurity = None
        self.ssidPassword = None
        self.enableInterface = None
        self.typeChannel = None

    def defaultSettings(self, cliente: ConnectHandler):
        '''
        Esta función se encarga de establecer la configuración por defecto en un router OpenWRT
        :return:
        '''
        defaultradio0 = ["uci set wireless.radio0=wifi-device", "uci set wireless.radio0.type='mac80211'",
                         "uci set wireless.radio0.path='ffe0a000.pcie/pcia000:02/a000:02:00.0/a000:03:00.0'",
                         "uci set wireless.radio0.htmode='VHT80'", "uci set wireless.radio0.option.country='ES'",
                         "uci set wireless.radio0.option.channel='36'", "uci set wireless.radio0.band='11ac'",
                         "uci set wireless.radio0.disabled='1'",
                         "uci set wireless.radio0.hwmode='11na'"]  # este ultimo es para limitar protocolo superior o igual a 802.11n

        defaultinteface0 = ["uci set wireless.default_radio0=wifi-iface",
                            "uci set wireless.default_radio0.device='radio0'",
                            "uci set wireless.default_radio0.network='lan'",
                            "uci set wireless.default_radio0.mode='ap'",
                            "uci set wireless.default_radio0.ssid='OpenWRT'",
                            "uci set wireless.default_radio0.encryption='none'"]

        defaultradio1 = ["uci set wireless.radio1=wifi-device", "uci set wireless.radio1.type='mac80211'",
                         "uci set wireless.radio1.path='ffe0a000.pcie/pcia000:02/a000:02:00.0/a000:03:00.0'",
                         "uci set wireless.radio1.option.channel='36'", "uci set wireless.radio1.htmode='HT20'",
                         "uci set wireless.radio1.band='11ac'", "uci set wireless.radio1.disabled='1'", ""
                                                                                                        "uci set wireless.radio1.country='ES'",
                         "uci set wireless.radio1.cell_density='0'",
                         "uci set wireless.radio1.hwmode='11na'"]  # este ultimo es para limitar protocolo superior o igual a 802.11n

        defaultinteface1 = ["uci set wireless.default_radio1=wifi-iface",
                            "uci set wireless.default_radio1.device='radio1'",
                            "uci set wireless.default_radio1.mode='ap'",
                            "uci set wireless.default_radio1.network='lan'",
                            "uci set wireless.default_radio1.ssid='OpenWRT'",
                            "uci set wireless.default_radio1.encryption='none'"]

        execute = ejecutar(cliente, defaultradio0)
        execute.exec()
        execute = ejecutar(cliente, defaultinteface0)
        execute.exec()
        execute = ejecutar(cliente, defaultradio1)
        execute.exec()
        execute = ejecutar(cliente, defaultinteface1)
        execute.exec()
        execute = ejecutar(cliente, ["uci commit wireless", "wifi"])
        execute.exec()

    def checkBytes(self, ssh: ConnectHandler) -> str:
        '''
        Esta función se encarga de verificar la cantidad de bytes en un archivo
        :param ssh(ConnectHandler): cliente SSH
        :return(str): cantidad de bytes en el archivo
        '''
        check_file = ejecutar(ssh, ["wc -c /etc/config/wireless | awk '{print $1}'"])  # checkBytes
        output = check_file.exec().strip()
        return output

    # Poner el tipo de seguridad
    def set_typeSecurity(self, encryptionType: str, typeRadio: int):
        self.typeSecurity = f"uci set wireless.default_radio{typeRadio}.encryption='{encryptionType}'"

    # Verificar el tipo de seguridad que se ha ingresado
    def check_typeSecurity(self) -> str:
        '''
        Esta función se encarga de solicitar el tipo de seguridad del SSID
        :param ssidSecurity(str): tipo de seguridad del SSID
        :return(str): tipo de seguridad del SSID
        '''
        while True:
            ssidSecurity = input("Ingrese la seguridad del SSID (WPA2-PSK, WPA3-SAE, WPA-PSK): ").strip().upper()
            if ssidSecurity in ("WPA2-PSK", "WPA3-SAE", "WPA-PSK"):
                # Asignar el valor correspondiente a encryptionType
                if ssidSecurity == "WPA2-PSK":
                    encryptionType = "psk2"
                elif ssidSecurity == "WPA3-SAE":
                    encryptionType = "sae"
                else:  # ssidSecurity == "WPA-PSK"
                    encryptionType = "psk"
                return encryptionType
                break  # Salir del bucle si la opción es válida
            else:
                print("Opción inválida. Por favor, ingrese una de las opciones válidas.")

    def typeChannelRadiate(self) -> str:
        '''
        Esta función se encarga de solicitar el canal a radiar
        :return(str): canal a radiar (2.4 o 5 Ghz)
        '''
        while True:
            channelRadiate = input(
                "Ingrese el canal a radiar (2.4 o 5 Ghz): ")  # radio0.channel = 2.4 y radio1.channel = 5
            # Comprobar si la opción ingresada es válida
            if channelRadiate in ("2.4", "5"):
                return channelRadiate
                break  # Salir del bucle si la opción es válida
            else:
                print("Opción inválida. Por favor, ingrese una de las opciones válidas.")
                return None

    # colocar tipo de canal
    def set_sizeChannel(self, typeRadio: int):
        self.typeChannel = f"uci set wireless.radio{typeRadio}.channel='{self.channelWidth}'"

    # colocar tipo de canal
    def set_channelWidth(self, channelWidth: int) -> str:
        self.channelWidth = channelWidth

    #obtener ancho de canal
    def get_channelWidth(self) -> str:
        return self.channelWidth
    #Añadir nombre del SSID
    def set_ssidName(self, ssidName: str, typeRadio: int):
        self.ssidName = f"uci set wireless.default_radio{typeRadio}.ssid='{ssidName}'"
    #Añadir contraseña del SSID
    def set_ssidPassword(self, password: str, typeRadio: int):
        self.ssidPassword = f"uci set wireless.default_radio{typeRadio}.key='{password}'"
    #Activar interfaz
    def set_enableInterface(self, typeRadio: int):
        self.enableInterface = f"uci set wireless.radio{typeRadio}.disabled='0'"
    #Añadir lista de comandos
    def set_listCommands(self, ssidName: str, encryptionType: str, password: str, channelRadiate: str) -> list[str]:
        '''
        Esta función se encarga de establecer la lista de comandos a ejecutar
        :param ssidName(str): nombre del SSID
        :param encryptionType(str): tipo de seguridad
        :param password(str): contraseña del SSID
        :return(list[str]): lista de comandos a ejecutar
        '''
        if channelRadiate == "5":  # radio1
            print("---------- 5 Ghz ----------")
            typeRadio = 1
            self.set_channelWidth(input("Ingrese el ancho de canal para 5 Ghz: "))
            self.set_sizeChannel(typeRadio)
            self.set_ssidName(ssidName, typeRadio)
            self.set_ssidPassword(password, typeRadio)
            self.set_typeSecurity(encryptionType, typeRadio)
            self.set_enableInterface(typeRadio)
            listCommands = [self.ssidName, self.ssidPassword, self.typeChannel, self.typeSecurity, self.enableInterface
                , self.keepChanges[0], self.keepChanges[1], self.keepChanges[2]]
        else:  # radio0
            print("---------- 2.4 Ghz ----------")
            typeRadio = 0
            self.set_ssidName(ssidName, typeRadio)
            self.set_sizeChannel(typeRadio)
            self.set_ssidPassword(password, typeRadio)
            self.set_typeSecurity(encryptionType, typeRadio)
            self.set_enableInterface(typeRadio)
            listCommands = [self.ssidName, self.typeSecurity, self.ssidPassword,
                            self.enableInterface, self.keepChanges[0], self.keepChanges[1], self.keepChanges[2]]

        return listCommands
    #Eliminar configuracion de SSID
    def deleteSettings(self) -> list[str]:
        listCommands = ["uci delete wireless.radio0", "uci delete wireless.default_radio0",
                        "uci delete wireless.radio1", "uci delete wireless.default_radio1", "uci commit wireless",
                        "wifi"]
        return listCommands
