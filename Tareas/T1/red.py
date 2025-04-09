import dcciudad
import os
import copy


class RedMetro:
    def __init__(self, red: list, estaciones: list) -> None:
        self.red = red
        self.estaciones = estaciones

    def informacion_red(self) -> list:
        primer_argumento = len(self.estaciones)
        segundo_argumento = []
        for i in self.red:
            segundo_argumento.append(sum(i))
        return [primer_argumento, segundo_argumento]

    def agregar_tunel(self, inicio: str, destino: str) -> int:
        if self.red[self.estaciones.index(inicio)][self.estaciones.index(destino)] == 0:
            self.red[self.estaciones.index(
                inicio)][self.estaciones.index(destino)] = 1
            return (sum(self.red[self.estaciones.index(inicio)]))
        else:
            return -1

    def tapar_tunel(self, inicio: str, destino: str) -> int:
        if self.red[self.estaciones.index(inicio)][self.estaciones.index(destino)] == 1:
            self.red[self.estaciones.index(
                inicio)][self.estaciones.index(destino)] = 0
            return (sum(self.red[self.estaciones.index(inicio)]))
        else:
            return -1

    def invertir_tunel(self, estacion_1: str, estacion_2: str) -> bool:
        tunel_1 = self.red[self.estaciones.index(
            estacion_1)][self.estaciones.index(estacion_2)]
        tunel_2 = self.red[self.estaciones.index(
            estacion_2)][self.estaciones.index(estacion_1)]
        if tunel_1 + tunel_2 == 2:
            return True
        elif tunel_1 == 1:
            self.red[self.estaciones.index(
                estacion_1)][self.estaciones.index(estacion_2)] = 0
            self.red[self.estaciones.index(
                estacion_2)][self.estaciones.index(estacion_1)] = 1
            return True
        elif tunel_2 == 1:
            self.red[self.estaciones.index(
                estacion_2)][self.estaciones.index(estacion_1)] = 0
            self.red[self.estaciones.index(
                estacion_1)][self.estaciones.index(estacion_2)] = 1
            return True
        else:
            return False

    def nivel_conexiones(self, inicio: str, destino: str) -> str:
        inicio_index = self.estaciones.index(inicio)
        destino_index = self.estaciones.index(destino)
        if dcciudad.alcanzable(self.red, inicio_index, destino_index):
            red_elevada_2 = dcciudad.elevar_matriz(self.red, 2)
            if self.red[inicio_index][destino_index] == 1:
                return "túnel directo"
            elif red_elevada_2[inicio_index][destino_index] > 0:
                return "estación intermedia"
            else:
                return "muy lejos"
        else:
            return "no hay ruta"

    def rutas_posibles(self, inicio: str, destino: str, p_intermedias: int) -> int:
        # si hay n ciudades intermedias, se requieren n + 1 tuneles
        inicio_index = self.estaciones.index(inicio)
        destino_index = self.estaciones.index(destino)
        red_elevada_p = dcciudad.elevar_matriz(self.red, p_intermedias + 1)
        return red_elevada_p[inicio_index][destino_index]

    def ciclo_mas_corto(self, estacion: str) -> int:
        estacion_index = self.estaciones.index(estacion)
        if self.red[estacion_index][estacion_index] == 1:
            return 0
        for i in range(2, len(self.estaciones) + 1):
            red_elevada_i = dcciudad.elevar_matriz(self.red, i)
            if red_elevada_i[estacion_index][estacion_index] > 0:
                return i - 1  # si pasa por n tuneles hay n - 1 estaciones intermedias
        return -1

    def estaciones_intermedias(self, inicio: str, destino: str) -> list:
        intermedias = []
        for i in range(len(self.red)):
            # si hay un tunel de estacion i a destino
            if self.red[i][self.estaciones.index(destino)] != 0:
                # si hay un tunel de inicio a estacion i
                if self.red[self.estaciones.index(inicio)][i] != 0:
                    intermedias.append(self.estaciones[i])
        return intermedias

    def estaciones_intermedias_avanzado(self, inicio: str, destino: str) -> list:
        # inicio -> intermedia 1 -> intermedia 2 -> final
        intermedias = []  # lista final
        intermedia_1 = []  # la cual conecta con la estacion de inicio
        intermedia_2 = []  # la cual conecta con la estacion destino
        inicio_index = self.estaciones.index(inicio)
        destino_index = self.estaciones.index(destino)
        for i in range(len(self.red)):
            if self.red[i][destino_index] != 0:
                # si hay un tunel de estacion (posibles) intermedia 2 a destino
                intermedia_2.append(self.estaciones[i])

        for j in range(len(intermedia_2)):
            intermedia_1.append([])
            # lista que contiene listas con estaciones que conectan
            for i in range(len(self.red)):
                if self.red[i][self.estaciones.index(intermedia_2[j])] != 0:
                    # si hay un tunel de estacion intermedia 1 a estacion intermedia 2
                    intermedia_1[j].append(self.estaciones[i])

        for i in range(len(intermedia_1)):
            for j in range(len(intermedia_1[i])):
                if self.red[inicio_index][self.estaciones.index(intermedia_1[i][j])] != 0:
                    # si inicio conecta conalguna de las posibles estaciones intermedia 1
                    intermedias.append([intermedia_1[i][j], intermedia_2[i]])
        print(intermedias)
        return intermedias

    def cambiar_planos(self, nombre_archivo: str) -> bool:
        ruta = os.path.join("data", nombre_archivo)
        if os.path.exists(ruta):
            with open(ruta, "r") as file:
                lineas_de_texto = file.readlines()
                numero_estaciones = int(lineas_de_texto[0])
                estaciones_nuevas = []
                for j in range(numero_estaciones):
                    estaciones_nuevas.append(lineas_de_texto[j + 1].strip())
                lista_completa = lineas_de_texto[numero_estaciones + 1].split(
                    ",")
                lista_completa = [int(x) for x in lista_completa]
                red_nueva = []
                for i in range(0, len(lista_completa), len(estaciones_nuevas)):
                    red_nueva.append(
                        lista_completa[i:(i + len(estaciones_nuevas))])
                self.estaciones = estaciones_nuevas
                self.red = red_nueva
                return True
        else:
            return False

    def asegurar_ruta(self, inicio: str, destino: str, p_intermedias: int) -> list:
        red_copia = copy.deepcopy(self.red)
        valor_inicio = self.estaciones.index(inicio)  # coordenada i
        valor_destino = self.estaciones.index(destino)  # coordenada j
        if self.rutas_posibles(inicio, destino, p_intermedias) == 0:
            # chequear si es posible ir de inicio a fin con p_intermedias
            return []
        if p_intermedias == 0:  # ver caso en que p_intermedias = 0
            if red_copia[valor_inicio][valor_destino] > 0:
                return red_copia
        else:  # para p_intermedias de 1 en adelante (al menos 2 tuneles)
            for i in range(len(self.estaciones)):
                for j in range(len(self.estaciones)):
                    variable_auxiliar = red_copia[i][j]
                    red_copia[i][j] = 0
                    if dcciudad.elevar_matriz(red_copia,
                                              p_intermedias + 1)\
                                                [valor_inicio][valor_destino] == 0:
                        red_copia[i][j] = variable_auxiliar
                        # revisar en cada elemento de la matriz si eliminandolo
                        # se puede seguir yendo
                        # a destino con p_intermedias
            j = 2
            while dcciudad.elevar_matriz(red_copia, j)[valor_inicio][valor_destino] == 0:
                j += 1
                # cantidad de tuneles hasta los que se pudieron dejar en 0
            if (j == p_intermedias + 1) and (red_copia[valor_inicio][valor_destino] == 0):
                # si coincide con los esperados (p_intermedias + 1) y
                # no existe tunel directo (se espera al menos 1 estacion intermedia)
                return red_copia
            else:
                return []
