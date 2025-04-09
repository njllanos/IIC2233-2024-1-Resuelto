from PyQt6.QtCore import pyqtSignal, QObject
import parametros as p

class VentanaInicioBackend(QObject):
    senal_mensaje_error = pyqtSignal()
    senal_empezar_partida = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def verificar_nombre_usuario(self, usuario: str):
        if usuario and usuario.isalnum():
            contiene_mayuscula = False
            contiene_numero = False
            for caracter in usuario:
                if caracter.isdigit():
                    contiene_numero = True
                if caracter.isupper():
                    contiene_mayuscula = True
            if contiene_mayuscula and contiene_numero:
                self.senal_empezar_partida.emit(usuario)
            else:
                self.senal_mensaje_error.emit()
        else:
            self.senal_mensaje_error.emit()

    def ordenar_puntajes(self):
        with open(p.RUTA_PUNTAJE_TXT, 'r') as archivo:
            lineas = archivo.readlines()
            lista_puntajes = list()
            for linea in lineas:
                partida = linea.strip("\n").split(",")
                lista_puntajes.append(partida)

        lista_puntajes_ordenada = sorted(lista_puntajes, key=lambda x: -float(x[1]))

        with open(p.RUTA_PUNTAJE_TXT, 'w') as doc:
            for i in range(len(lista_puntajes_ordenada)):
                if i != len(lista_puntajes_ordenada) - 1:
                    doc.write(f"{lista_puntajes_ordenada[i][0]},{lista_puntajes_ordenada[i][1]}\n")
                else:
                    doc.write(f"{lista_puntajes_ordenada[i][0]},{lista_puntajes_ordenada[i][1]}")
                
