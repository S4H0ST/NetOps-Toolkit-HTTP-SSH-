import pandas as pd

def write_excel(array_correos: list[str],array_respuestas: list[str], nombre_archivo: str):
    '''
        Escribe los correos electrónicos y sus respuestas asociadas en un archivo Excel.

        Si el archivo especificado por `nombre_archivo` ya existe, lee su contenido y agrega las nuevas respuestas. Si no existe,
        crea un nuevo archivo Excel con los datos proporcionados.

        :param array_correos(list[str]): Lista de correos electrónicos a escribir en el archivo Excel.
        :param array_respuestas(list[str]): Lista de respuestas asociadas a los correos electrónicos.
        :param nombre_archivo(str): Nombre del archivo Excel donde se guardarán los datos.
        '''
    # Leer el archivo Excel existente
    try:
        df_existente = pd.read_excel(nombre_archivo)
    except FileNotFoundError:
        # Si el archivo no existe, crear un DataFrame vacío
        df_existente = pd.DataFrame(columns=['Correo', 'Respuesta'])

    # Verificar si el número de correos coincide con el número de respuestas
    if len(array_correos) != len(array_respuestas):
        raise ValueError("El número de correos no coincide con el número de respuestas")

    # Crear un DataFrame con los correos y respuestas correspondientes
    df_nuevas_respuestas = pd.DataFrame({'Correo': array_correos, 'Respuesta': array_respuestas})

    # Guardar el DataFrame actualizado en el archivo Excel
    df_nuevas_respuestas.to_excel(nombre_archivo, index=False)


