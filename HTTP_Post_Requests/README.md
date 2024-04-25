Peticiones Http
--
---
Documentación para la creación y recopilación de solicitud y respuesta POST de HTTP sobre excel.

1. [Main.py](./main.py) es el ejecutable donde se encuentran las llamadas a las funciones.
2. [Archivo.xlsx](./archivo.xlsx) contendrá en la primera columna con  nombre, teléfono (o extensión) o e-mail. La segunda columna contendrá una vez ejecutado [main.py](./main.py) las respuestas a cada solicitud POST.
3. [ExcelRead.py](./excelRead.py) tiene una funcion de lectura de excel, que devuelve un array con los elementos de la primera columna.
````python
def lectura(nombre_archivo:str) -> list[str]:
    
    datos_col1 = pd.read_excel(nombre_archivo, usecols=[0])
    lcorreo = datos_col1['Correo'].values
    
    return lcorreo
````
4. [EnvioPost.py](./envioPost.py) tiene dos funciones para el envio y la obtención del dato que buscamos:

``envio_post`` para el envio y recoger la respuesta literal de la solicitud
```python
def envio_post(array_correos:list[str]):
    url = ' ' #añadir servidor web
    array_respuestas = []

    for correo in array_correos:
        payload = {'buscador': correo} # aqui añadir {clave, valor}
        response = requests.post(url, data=payload)
        contenido_correo = obtener_src(response.text)
        array_respuestas.append(contenido_correo)

    return array_respuestas
```
``obtener_src`` para filtrar la respuesta y capturar solo el src de la respuesta
```python
def obtener_src(html: str)->str:
    
    soup = BeautifulSoup(html, 'html.parser')
    correo_content = soup.find('i', class_='fa fa-envelope').find_next('img').get('src')
    
    return correo_content
```
5. [ExcelWrite.py](./excelWrite.py) encargado de concatenar la respuesta en la columna correspondiente a las **Respuestas**
```python
def write_excel(array_correos: list[str],array_respuestas: list[str], nombre_archivo: str):
   
    try:
        df_existente = pd.read_excel(nombre_archivo)
    except FileNotFoundError:
 
        df_existente = pd.DataFrame(columns=['Correo', 'Respuesta'])

    if len(array_correos) != len(array_respuestas):
        raise ValueError("El número de correos no coincide con el número de respuestas")

    df_nuevas_respuestas = pd.DataFrame({'Correo': array_correos, 'Respuesta': array_respuestas})

    df_nuevas_respuestas.to_excel(nombre_archivo, index=False)
```
Nota: [archivo.xlsx](./archivo.xlsx) no se debe de manipular directamente.