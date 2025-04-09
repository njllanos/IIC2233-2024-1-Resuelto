import sys
import os
import dcciudad
from red import RedMetro

if len(sys.argv) != 3:  # Se verifica que el formato sea correcto
    # Creo que esto esta incluido en supuesto 1.3 de READ.me (pero por si acaso)
    print("Formato incorrecto")
    sys.exit()

nombre_archivo = sys.argv[1]
estacion = sys.argv[2]
ruta = os.path.join("data", str(nombre_archivo) + ".txt")

if not os.path.exists(ruta):
    # Verificar si red existe
    print("La red no existe.")
    sys.exit()

with open(ruta, "r") as file:
    # procesar archivo .txt (similar a la funcion cambiar_planos de Parte 1)
    lineas_de_texto = file.readlines()
    numero_estaciones = int(lineas_de_texto[0])
    estaciones = []
    for j in range(numero_estaciones):
        estaciones.append(lineas_de_texto[j + 1].strip())
    lista_completa = lineas_de_texto[numero_estaciones + 1].split(",")
    lista_completa = [int(x) for x in lista_completa]
    red = []
    for i in range(0, len(lista_completa), len(estaciones)):
        red.append(lista_completa[i:(i + len(estaciones))])

if not estacion in estaciones:
    # Verificar si estación existe
    print("Estación no existe.")
    sys.exit()

red_metro = RedMetro(red, estaciones)
# definir objeto con archivo procesado


def mostrar_menu(diccionario_opciones):
    # Print de menu y sus opciones
    print(f"¡Se cargó la red {str(nombre_archivo)}.txt!")
    print(f"La estación elegida es: {estacion}")
    print("*** Menú de Acciones ***")
    for opcion in diccionario_opciones:
        print(f" [{opcion}] {diccionario_opciones[opcion]}")


def leer_opcion(diccionario_opciones):
    # Captura la opcion elegida
    opcion_elegida = "0"
    while opcion_elegida not in ["1", "2", "3", "4"]:
        opcion_elegida = input("Indique su opcion (1, 2, 3 o 4): ")
        if opcion_elegida not in ["1", "2", "3", "4"]:
            print("Opción no valida, vuelve a intentarlo.")
    return opcion_elegida


def ejecutar_opcion(opcion_elegida, diccionario_opciones):
    # ejecuta la opcion elegida respectivamente
    if opcion_elegida == "1":
        dcciudad.imprimir_red(red, estaciones)

    elif opcion_elegida == "2":
        print(red_metro.ciclo_mas_corto(estacion))

    elif opcion_elegida == "3":
        destino = str(input("Ingresa el nombre de la estación de destino: "))
        p_intermedias = int(
            input("Ingresa el número de estaciones intermedias: "))
        print(red_metro.asegurar_ruta(estacion, destino, p_intermedias))

    elif opcion_elegida == "4":
        sys.exit()


def generar_menu(diccionario_opciones, opcion_salida):
    # hace el loop de: menu -> opcion -> ejecucion opcion; hasta la salida
    opcion_elegida = None
    while opcion_elegida != opcion_salida:
        mostrar_menu(diccionario_opciones)
        opcion_elegida = leer_opcion(diccionario_opciones)
        ejecutar_opcion(opcion_elegida, diccionario_opciones)
        print()


def menu_principal():
    # define diccionario para ser usado en las funciones del loop para el menu
    diccionario_opciones = {
        "1": ("Mostrar red"),
        "2": ("Encontrar ciclo más corto"),
        "3": ("Asegurar ruta"),
        "4": ("Salir del programa")
    }

    # desencadena el loop del menu para cumplir sus funciones
    generar_menu(diccionario_opciones, "4")


if __name__ == '__main__':
    menu_principal()
