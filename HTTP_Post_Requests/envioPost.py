import requests
from bs4 import BeautifulSoup

def obtener_src(html: str)->str:
    '''
    Extrae la dirección de correo electrónico de un fragmento de HTML.

    :param html(str): Fragmento de HTML donde se buscará la dirección de correo electrónico.
    :return: Dirección de correo electrónico extraída del HTML.
    :rtype: str
    '''
    soup = BeautifulSoup(html, 'html.parser') #inicializa el objeto BeautifulSoup para manipular el excel
    correo_content = soup.find('i', class_='fa fa-envelope').find_next('img').get('src') #lectura y captura del patron dentro del html
    return correo_content
def envio_post(array_correos:list[str])->list[str]:
    '''
    Realiza solicitudes POST a una página web para cada correo electrónico en el array
    y guarda las respuestas en un array.
    :param array_correos(list[str]): Lista de correos electrónicos para buscar en la página web.
    :return: Lista de respuestas obtenidas para cada correo electrónico.
    :rtype: list[str]
    '''
    # URL de la página web
    url = 'https://gestion2.urjc.es/directorio/'
    # Array para guardar las respuestas
    array_respuestas = []

    # Realizar solicitudes POST para cada correo en el array
    for correo in array_correos:
        payload = {'buscador': correo} #la información/parametros de busqueda
        response = requests.post(url, data=payload) #info. necesaria para buscar
        contenido_correo = obtener_src(response.text) #recopilación de la respuesta
        array_respuestas.append(contenido_correo) #agregar la respuesta en el array

    return array_respuestas
