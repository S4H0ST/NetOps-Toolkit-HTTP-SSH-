import excelRead
from envioPost import envio_post
from excelWrite import write_excel


def main():
    contador = 1
    contador2 = 1
    nameFile = "archivo.xlsx"
    excel = excelRead
    lista_correos = excel.lectura(nameFile)
    print("#############")

    print("Contenido de la primera columna del archivo Excel:")
    for correo in lista_correos:
        print(f"{contador} : {correo}" )
        contador+=1
    print("#############")

    respuestas = envio_post(lista_correos)
    print("Respuestas a la peticion post del archivo Excel:")
    for respuesta in respuestas:
        print(f"{contador2} : {respuesta}")
        contador2 += 1

    write_excel(lista_correos,respuestas, nameFile)
if __name__ == "__main__":
    main()