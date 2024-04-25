import pandas as pd

def lectura(nombre_archivo:str) -> list[str]:
    '''
        Lee el contenido de la primera columna de un archivo Excel.

        :param nombre_archivo(str): El nombre del archivo Excel del cual leer.
        :return: Una lista de correos electrónicos extraídos de la primera columna del archivo.
        :rtype: list[str]
        '''
    # Lee solo la primera columna del archivo Excel
    datos_col1 = pd.read_excel(nombre_archivo, usecols=[0]) #Indica la lectura de solo la columna 0.
    lcorreo = datos_col1['Correo'].values #asume que existe una columna llamada correo y coge todos sus valores.

    # Muestra los datos leídos
    print(datos_col1)
    return lcorreo