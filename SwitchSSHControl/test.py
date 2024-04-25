import unittest
from puertos import ejecutar_puertos
from IPs import IPs
from puertos import puertos
from PortControl.configuracion import configuracion


class TestEjecutarPuertos(unittest.TestCase):
    def test_ejecutar_puertos(self):
        config = configuracion(usuario="user", clave="clave")
        # IPs
        ip1 = IPs(dirIp="192.168.1.1",
                  puertos=[puertos(numPuerto=22, estado="enable"), puertos(numPuerto=33, estado="show")])
        r1 = "IP=192.168.1.1;PUERTO=22;COMANDO=enable\nIP=192.168.1.1;PUERTO=33;COMANDO=show\n"
        print("TEST 1")
        self.assertEqual(ejecutar_puertos(config, ip1).ejecutar(), r1)

        ip1 = IPs(dirIp="192.168.a.1",
                  puertos=[puertos(numPuerto=22, estado="enable"), puertos(numPuerto=33, estado="show")])
        r1 = "IP INCORRECTA\n"
        print("TEST 2")
        self.assertEqual(ejecutar_puertos(config, ip1).ejecutar(), r1)

        ip1 = IPs(dirIp="192.168.1.1",
                  puertos=[puertos(numPuerto=22, estado="bocadillo"), puertos(numPuerto=33, estado="show")])
        r1 = "COMANDO INCORRECTO\n"
        print("TEST 3")
        self.assertEqual(ejecutar_puertos(config, ip1).ejecutar(), r1)

        ip1 = IPs(dirIp="192.168.1.1",
                  puertos=[puertos(numPuerto=-3, estado="enable"), puertos(numPuerto=33, estado="show")])
        r1 = "PUERTO INCORRECTO\n"
        print("TEST 4")
        self.assertEqual(ejecutar_puertos(config, ip1).ejecutar(), r1)


if __name__ == '__main__':
    unittest.main()