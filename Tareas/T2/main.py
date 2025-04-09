from sys import exit, argv
from funciones import (cargar_archivo_dificultad, cargar_unidades, menu_de_inicio_prints, 
                        crear_ejercito, menu_de_tienda_prints, procesar_compra)
from ejercito import Ejercito

if len(argv) != 2: # Verifica cantidad de argumentos
    print("\nEl formato para ejecutar el programa es incorrecto.")
    print("Asegurate que sea de la forma: python/py/python3 main.py facil/medio/dificil.\n")
    exit()
if argv[1] not in ["facil", "intermedio", "dificil"]: 
    # Verifica que argumento sea una dificultad
    print("\nError de formato, debes elegir una dificultad entre facil/intermedio/dificil.\n")
    exit()

dificultad = argv[1] 

ejercito_usuario = Ejercito()

# Se leen los archivos pertinentes
ejercitos_rondas = cargar_archivo_dificultad(dificultad)
unidades = cargar_unidades()

def menu_de_inicio(ejercito, unidades, ejercitos_rondas):
    eleccion = menu_de_inicio_prints(ejercito)
    while eleccion not in [str(i) for i in range(0, 4)]:
        print("\nOpción no valida. Vuelva a intentarlo.")
        eleccion = menu_de_inicio_prints(ejercito)

    if eleccion == "1":
        eleccion_tienda = menu_de_tienda_prints(ejercito)
        while eleccion_tienda != "0":
            while eleccion_tienda not in [str(i) for i in range(0, 8)]:
                print("\nOpción no valida. Vuelva a intentarlo.")
                eleccion_tienda = menu_de_tienda_prints(ejercito)
            if eleccion_tienda != "0":
                ejercito = procesar_compra(eleccion_tienda, ejercito, unidades)
                eleccion_tienda = menu_de_tienda_prints(ejercito)
        menu_de_inicio(ejercito, unidades, ejercitos_rondas)

    elif eleccion == "2":
        print(ejercito)
        menu_de_inicio(ejercito, unidades, ejercitos_rondas)

    elif eleccion == "3":
        ejercito_rival = crear_ejercito(ejercitos_rondas[ejercito.ronda - 1])
        ejercito = ejercito.combatir(ejercito_rival)
        ejercitos_rondas = cargar_archivo_dificultad(dificultad) 
        # Volver a cargar los archivos de rondas para reenovarlos luego de combate
        if ejercito.ronda == 4:
            print("\nJuego terminado, ¡Haz ganado!")
            if dificultad in ["facil", "intermedio"]: # print segun dificultad que fue ganada
                print("¿Podrás hacer lo mismo con una dificultad mayor?\n")
            else:
                print("Venciste a Gatochico en su dificultad mayor, ¡Felicidades!\n")
                # print si gana con dificultad dificl
            exit()
        menu_de_inicio(ejercito, unidades, ejercitos_rondas)

    elif eleccion == "0":
        print("\nCerrando el programa, gracias por jugar.\n")
        exit()


menu_de_inicio(ejercito_usuario, unidades, ejercitos_rondas)
