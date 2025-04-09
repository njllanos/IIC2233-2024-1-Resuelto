import os
from sys import exit, argv
import random
import parametros
from items import Armadura, Pergamino, Lanza
from combatientes import Mago, Caballero, Guerrero, Paladín, MagoDeBatalla, CaballeroArcano
from ejercito import Ejercito

###################### Funciones para leer archivos ######################


# se extiende str para checkear el contenido de los archivos mas facilmente
class Check(str):
    def tipo(self): # verificar que el tipo de combatiente es correcto
        if self in ["MAG", "CAB", "GUE", "CAR", "PAL", "MDB"]:
            return True
        else:
            return False

    def basico(self): # verificar que el tipo de combatiente es uno de los 3 basicos
        if self in ["MAG", "CAB", "GUE"]:
            return True
        else:
            return False

    def vida_max(self): # verificar los rangos de vida_maxima
        if (self.isdigit()) and \
                (parametros.MIN_VIDA <= int(self)) and (int(self) <= parametros.MAX_VIDA):
            return True
        else:
            return False

    def poder(self): # verificar los rangos de poder
        if (self.isdigit()) and \
                (parametros.MIN_PODER <= int(self)) and (int(self) <= parametros.MAX_PODER):
            return True
        else:
            return False

    def agilidad(self): # verificar los rangos de agilidad
        if (self.isdigit()) and \
                (parametros.MIN_AGILIDAD <= int(self)) and (int(self) <= parametros.MAX_AGILIDAD):
            return True
        else:
            return False

    def resistencia(self): # verificar los rangos de resistencia
        if (self.isdigit()) and \
            (parametros.MIN_RESISTENCIA <= int(self)) and \
                (int(self) <= parametros.MAX_RESISTENCIA):
            return True
        else:
            return False

    def defensa(self): # se verifica los rangos de defensa
        if (self.isdigit()) and \
                (parametros.MIN_DEFENSA <= int(self)) and (int(self) <= parametros.MAX_DEFENSA):
            return True
        else:
            return False


def cargar_archivo_dificultad(dificultad) -> list: 
    # devuelve lista de listas con combatientes de cada ronda segun la dificultad seleccionada
    # y verifica el formato del archivo
    ruta = os.path.join("data", str(dificultad) + ".txt")
    if not os.path.exists(ruta):
        print("\nHay un problema con la ruta del archivo de la dificultad seleccionada.\n")
        exit()
    with open(ruta, "r") as file:
        mensaje = "\nEl archivo de la dificulatad seleccionada no tiene el formato correcto.\n"
        lineas_archivo = file.readlines()
        if len(lineas_archivo) != 3:
            print(mensaje)
            exit()
        lineas_por_ronda = [linea.strip().split(";") for linea in lineas_archivo]
        ronda_1 = []
        ronda_2 = []
        ronda_3 = []
        for i in range(len(lineas_por_ronda)):
            for gato in lineas_por_ronda[i]:
                gato = gato.split(",")
                if (len(gato) != 7):
                    print(mensaje)
                    exit()
                premisa = (Check(gato[1]).tipo() and Check(gato[2]).vida_max())
                premisa_2 = (Check(gato[3]).defensa() and Check(gato[4]).poder())
                premisa_3 = (Check(gato[5]).agilidad() and Check(gato[6]).resistencia())
                if not (premisa and premisa_2 and premisa_3):
                    print(mensaje)
                    exit()
                else:
                    gato_final = identificador_tipo(gato)
                    if i == 0:
                        ronda_1.append(gato_final)
                    if i == 1:
                        ronda_2.append(gato_final)
                    if i == 2:
                        ronda_3.append(gato_final)
    return [ronda_1, ronda_2, ronda_3]


def cargar_unidades() -> list: 
    # devuelve lista con todos los gatos de "unidades"
    # y verifica el formato del archivo
    ruta = os.path.join("data", "unidades.txt")
    if not os.path.exists(ruta):
        print("\nHay un problema con la ruta del archivo de las unidades disponibles.\n")
        exit()
    with open(ruta, "r") as file:
        lineas_archivo = file.readlines()
        todos_los_gatos = []
        hay_guerrero = False
        hay_caballero = False
        hay_mago = False
        for linea in lineas_archivo:
            gato = linea.strip().split(",")
            premisa = (Check(gato[1]).basico() and Check(gato[2]).vida_max())
            premisa_2 = (Check(gato[3]).defensa() and Check(gato[4]).poder())
            premisa_3 = (Check(gato[5]).agilidad() and Check(gato[6]).resistencia())
            if not (premisa and premisa_2 and premisa_3 and len(gato) == 7):
                print("\nEl archivo de las unidades disponibles no tiene el formato correcto.\n")
                exit()
            else:
                if gato[1] == "GUE":
                    hay_guerrero = True
                if gato[1] == "CAB":
                    hay_caballero = True
                if gato[1] == "MAG":
                    hay_mago = True
                gato_final = identificador_tipo(gato)
                todos_los_gatos.append(gato_final)
        if not (hay_guerrero and hay_caballero and hay_mago): # Que esten todos los basicos
            print("\nEl archivo de las unidades disponibles no tiene el formato correcto.\n")
            exit()
        else:
            return todos_los_gatos


def identificador_tipo(gato: list) -> list:
    # toma la lista con las caracteristicas del gato segun formato de funciones anteriores:
    # ["Nombre", "tipo", "defensa", ...]
    # y devulve el gato ya creado como objeto
    if gato[1] == "MAG":
        gato = Mago(gato[0], int(gato[2]), int(gato[4]),
                    int(gato[3]), int(gato[5]), int(gato[6]))
    elif gato[1] == "CAB":
        gato = Caballero(gato[0], int(gato[2]), int(
            gato[4]), int(gato[3]), int(gato[5]), int(gato[6]))
    elif gato[1] == "GUE":
        gato = Guerrero(gato[0], int(gato[2]), int(
            gato[4]), int(gato[3]), int(gato[5]), int(gato[6]))
    elif gato[1] == "CAR":
        gato = CaballeroArcano(gato[0], int(gato[2]), int(
            gato[4]), int(gato[3]), int(gato[5]), int(gato[6]))
    elif gato[1] == "PAL":
        gato = Paladín(gato[0], int(gato[2]), int(gato[4]),
                       int(gato[3]), int(gato[5]), int(gato[6]))
    elif gato[1] == "MDB":
        gato = MagoDeBatalla(gato[0], int(gato[2]), int(
            gato[4]), int(gato[3]), int(gato[5]), int(gato[6]))
    return gato

###################### Funciones para menus y main ######################


def crear_ejercito(lista_ejercito) -> list: 
    # crea un ejercito a partir de una lista de gatos
    ejercito = Ejercito()
    for combatiente in lista_ejercito:
        ejercito.combatientes.append(combatiente)
    return ejercito


def menu_de_inicio_prints(ejercito) -> str:
    print("\n*** Menú de Inicio ***\n")
    print(f"Dinero disponible: {ejercito.oro}")
    print(f"Ronda actual: {ejercito.ronda}\n")
    print("[1] Tienda")
    print("[2] Ejercito")
    print("[3] Combatir\n")
    print("[0] Salir del programa\n")
    input_respuesta = input("Indique su opción: ")
    return input_respuesta


def menu_de_tienda_prints(ejercito) -> str:
    print("\n*** Tienda ***\n")
    print(f"Dinero disponible: {ejercito.oro}\n")
    print(f"       Producto      Precio")
    print(f"[1] Gato Mago          {parametros.PRECIO_MAG}")
    print(f"[2] Gato Guerrero      {parametros.PRECIO_GUE}")
    print(f"[3] Gato Caballero     {parametros.PRECIO_CAB}")
    print(f"[4] Item Armadura      {parametros.PRECIO_ARMADURA}")
    print(f"[5] Item Pergamino     {parametros.PRECIO_PERGAMINO}")
    print(f"[6] Item Lanza         {parametros.PRECIO_LANZA}")
    print(f"[7] Curar ejercito     {parametros.PRECIO_CURA}\n")
    print(f"[0] Volver al Menú de Inicio\n")
    input_respuesta = input("Indique su opción: ")
    return input_respuesta


def menu_de_items_prints(aplicables) -> str:
    print("\n*** Seleciona un gato ***\n")
    print(f"     Clase          Nombre")
    for i in range(len(aplicables)):
        print(f"[{i + 1}] Gato {aplicables[i].tipo: <10s} {aplicables[i].nombre}")
    eleccion_usuario = input("\nIndique su opción: ")
    return eleccion_usuario


def procesar_compra(eleccion_tienda, ejercito, unidades) -> Ejercito:
    # procesa la compra en tienda segun elección
    unidades = cargar_unidades()
    # Actualiza nuevamente unidades para que no tengan diferencias de vida
    mensaje_error_item_1 = "\nError en la compra: el item seleccionado "
    mensaje_error_item_2 = "no es compatible con ningun gato de tu ejercito."
    if eleccion_tienda == "1":
        if ejercito.oro < parametros.PRECIO_MAG:
            print("\nError en la compra: oro insuficiente.")
            return ejercito
        magos = [gato for gato in unidades if gato.tipo == "Mago"]
        ejercito.combatientes.append(random.choice(magos))
        ejercito.oro -= parametros.PRECIO_MAG

    elif eleccion_tienda == "2":
        if ejercito.oro < parametros.PRECIO_GUE:
            print("\nError en la compra: oro insuficiente.")
            return ejercito
        guerreros = [gato for gato in unidades if gato.tipo == "Guerrero"]
        ejercito.combatientes.append(random.choice(guerreros))
        ejercito.oro -= parametros.PRECIO_GUE

    elif eleccion_tienda == "3":
        if ejercito.oro < parametros.PRECIO_CAB:
            print("\nError en la compra: oro insuficiente.")
            return ejercito
        caballeros = [gato for gato in unidades if gato.tipo == "Caballero"]
        ejercito.combatientes.append(random.choice(caballeros))
        ejercito.oro -= parametros.PRECIO_CAB

    elif eleccion_tienda == "4":
        if ejercito.oro < parametros.PRECIO_ARMADURA:
            print("\nError en la compra: oro insuficiente.")
            return ejercito
        item = Armadura()
        aplicables = item.identificar_aplicables(ejercito)
        if len(aplicables) == 0:
            print(mensaje_error_item_1 + mensaje_error_item_2)
            return ejercito
        else:
            ejercito.oro -= parametros.PRECIO_ARMADURA
            eleccion_usuario = menu_de_items_prints(aplicables)
            while eleccion_usuario not in [str(i + 1) for i in range(len(aplicables))]:
                print("\nOpción no valida. Vuelva a intentarlo.")
                eleccion_usuario = menu_de_items_prints(aplicables)
            gato_elegido = aplicables[int(eleccion_usuario) - 1]
            ejercito.combatientes[ejercito.combatientes.index(gato_elegido)] = \
                gato_elegido.evolucionar(item)

    elif eleccion_tienda == "5":
        if ejercito.oro < parametros.PRECIO_PERGAMINO:
            print("\nError en la compra: oro insuficiente.")
            return ejercito
        item = Pergamino()
        aplicables = item.identificar_aplicables(ejercito)
        if len(aplicables) == 0:
            print(mensaje_error_item_1 + mensaje_error_item_2)
            return ejercito
        else:
            ejercito.oro -= parametros.PRECIO_PERGAMINO
            eleccion_usuario = menu_de_items_prints(aplicables)
            while eleccion_usuario not in [str(i + 1) for i in range(len(aplicables))]:
                print("\nOpción no valida. Vuelva a intentarlo.")
                eleccion_usuario = menu_de_items_prints(aplicables)
            gato_elegido = aplicables[int(eleccion_usuario) - 1]
            ejercito.combatientes[ejercito.combatientes.index(gato_elegido)] = \
                gato_elegido.evolucionar(item)

    elif eleccion_tienda == "6":
        if ejercito.oro < parametros.PRECIO_LANZA:
            print("\nError en la compra: oro insuficiente.")
            return ejercito
        item = Lanza()
        aplicables = item.identificar_aplicables(ejercito)
        if len(aplicables) == 0:
            print(mensaje_error_item_1 + mensaje_error_item_2)
            return ejercito
        else:
            ejercito.oro -= parametros.PRECIO_LANZA
            eleccion_usuario = menu_de_items_prints(aplicables)
            while eleccion_usuario not in [str(i + 1) for i in range(len(aplicables))]:
                print("\nOpción no valida. Vuelva a intentarlo.")
                eleccion_usuario = menu_de_items_prints(aplicables)
            gato_elegido = aplicables[int(eleccion_usuario) - 1]
            ejercito.combatientes[ejercito.combatientes.index(gato_elegido)] = \
                gato_elegido.evolucionar(item)

    elif eleccion_tienda == "7":
        if ejercito.oro < parametros.PRECIO_CURA:
            print("\nError en la compra: oro insuficiente.")
            return ejercito
        ejercito.oro -= parametros.PRECIO_LANZA
        for gato in ejercito.combatientes:
            gato.curarse(parametros.CURAR_VIDA)
    elif eleccion_tienda == "0": # No deberia pasar nunca por estructura de codigo
        return ejercito
    print("\n¡Compra realizada con éxito!")
    return ejercito
