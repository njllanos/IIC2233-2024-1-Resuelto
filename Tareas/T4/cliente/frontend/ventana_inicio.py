from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, 
                            QScrollArea, QPushButton, QMessageBox)
from PyQt6.QtGui import QFont, QPixmap, QMouseEvent, QKeyEvent
from PyQt6.QtCore import Qt, pyqtSignal, QObject
import parametros as p
from frontend.funciones_frontend import borrar_layout, limpiar_layout
import os

class VentanaInicio(QWidget):
    senal_verificar_nombre = pyqtSignal(str)
    senal_jugar_partida = pyqtSignal(str, str)
    senal_ordenar_puntajes = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.init_gui()

    def init_gui(self) -> None:
        self.setGeometry(50, 50, 800, 650)
        self.setFixedSize(800, 650)
        self.setWindowTitle("Ventana de Inicio")

        self.layout_compilado = QVBoxLayout()

        self.layout_logo = QLabel()
        self.layout_logo.setPixmap(QPixmap(QPixmap(p.RUTA_LOGO).scaled(250, 250)))
        self.layout_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_compilado.addWidget(self.layout_logo)

        self.layout_abajo = QHBoxLayout()

        self.layout_izquierda = QVBoxLayout()
        self.titulo_izquierda = QLabel("Salon de la Fama:")
        self.titulo_izquierda.setFont(QFont("Arial", 12))
        self.layout_izquierda.addWidget(self.titulo_izquierda)


        self.widget_salon_de_la_fama = QScrollArea()
        self.widget_salon_de_la_fama.setWidgetResizable(True)
        self.widget_scroll = QWidget()
        self.layout_scroll = QHBoxLayout()
        self.widget_scroll.setLayout(self.layout_scroll)
        self.layout_ranking = QVBoxLayout()
        self.layout_nombres = QVBoxLayout()
        self.layout_puntajes = QVBoxLayout()

        self.layout_scroll.addLayout(self.layout_ranking)
        self.layout_scroll.addLayout(self.layout_nombres)
        self.layout_scroll.addLayout(self.layout_puntajes)
        self.widget_scroll.setLayout(self.layout_scroll)
        self.widget_salon_de_la_fama.setWidget(self.widget_scroll)

        self.actualizar_salon_de_fama()
        self.layout_izquierda.addWidget(self.widget_salon_de_la_fama)
        
        self.layout_abajo.addLayout(self.layout_izquierda)

        self.layout_derecha = QVBoxLayout()

        self.layout_nombre_puzzle = QVBoxLayout()

        self.layout_usuario = QHBoxLayout()
        self.titulo_input = QLabel("Nombre de Usuario:")
        self.titulo_input.setFont(QFont("Arial", 12))
        self.nombre_usuario = QLineEdit("", self)
        self.nombre_usuario.setFont(QFont("Arial", 12))
        self.layout_usuario.addWidget(self.titulo_input)
        self.layout_usuario.addWidget(self.nombre_usuario)
        self.layout_nombre_puzzle.addLayout(self.layout_usuario)

        self.layout_selector = QHBoxLayout()
        self.titulo_selector = QLabel("Selecciona un puzzle:")
        self.titulo_selector.setFont(QFont("Arial", 12))
        self.selector_puzzles = QComboBox()
        self.lista_puzzles = os.listdir(p.RUTA_BASE_PUZZLES)
        self.lista_puzzles = sorted(self.lista_puzzles, key=str.lower, reverse = True)
        self.selector_puzzles.addItems(self.lista_puzzles)
        self.selector_puzzles.setFont(QFont("Arial", 12))
        self.layout_selector.addWidget(self.titulo_selector)
        self.layout_selector.addWidget(self.selector_puzzles)
        self.layout_nombre_puzzle.addLayout(self.layout_selector)
        self.layout_nombre_puzzle.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.layout_derecha.addLayout(self.layout_nombre_puzzle)

        self.layout_botones = QHBoxLayout()
        self.boton_comenzar = QPushButton("Comenzar partida")
        self.boton_comenzar.setStyleSheet(f"""background-color: green; border-style: outset; 
                                    border-width: 2px;border-radius: 10px; border-color: beige; 
                                    font: bold 14px; min-width: 10em; padding: 6px;""")
        self.boton_comenzar.clicked.connect(self.verificar_nombre_usuario)
        self.boton_salir = QPushButton("Salir")
        self.boton_salir.setStyleSheet(f"""background-color: red; border-style: outset; 
                                    border-width: 2px;border-radius: 10px; border-color: beige; 
                                    font: bold 14px; min-width: 10em; padding: 6px;""")
        self.boton_salir.clicked.connect(self.salir)
        self.layout_botones.addWidget(self.boton_comenzar)
        self.layout_botones.addWidget(self.boton_salir)
        self.layout_derecha.addLayout(self.layout_botones)

        self.layout_abajo.addLayout(self.layout_derecha)

        self.layout_compilado.addLayout(self.layout_abajo)

        self.setLayout(self.layout_compilado)

        self.show()

    def actualizar_salon_de_fama(self):
        self.senal_ordenar_puntajes.emit()
        self.layout_ranking.addWidget(QLabel("Puesto"))
        self.layout_nombres.addWidget(QLabel("Usuarios"))
        self.layout_puntajes.addWidget(QLabel("Puntajes"))
        with open(p.RUTA_PUNTAJE_TXT, 'r') as archivo:
            lineas = archivo.readlines()
            for i in range(len(lineas)):
                linea = lineas[i].strip("\n").split(",")
                rank = f"{i + 1}"
                nombre = linea[0]
                puntaje = linea[1]
                self.layout_ranking.addWidget(QLabel(f"{rank}"))
                self.layout_nombres.addWidget(QLabel(f"{nombre}"))
                self.layout_puntajes.addWidget(QLabel(f"{puntaje}"))
        self.widget_salon_de_la_fama.setWidget(self.widget_scroll)


    def verificar_nombre_usuario(self):
        self.senal_verificar_nombre.emit(self.nombre_usuario.text())

    def mensaje_error(self):
        pop_mensaje_error = QMessageBox()
        pop_mensaje_error.setWindowTitle("Error nombre de Usuario")
        pop_mensaje_error.setText(f"""Nombre de Usario Invalido.
Ingrese un nombre alphanumerico no vacio que contenga lo siguiente: 
    1) Un número
    2) Una letra mayuscula""")
        pop_mensaje_error.exec()
        self.nombre_usuario.clear()

    def salir(self):
        self.close()

    def comenzar(self, usuario: str):
        puzzle_seleccionado = self.selector_puzzles.currentText()
        self.senal_jugar_partida.emit(usuario, puzzle_seleccionado)
        self.close()

    def mostrar_ventana(self):
        self.nombre_usuario.clear()
        limpiar_layout(self.layout_nombres)
        limpiar_layout(self.layout_ranking)
        limpiar_layout(self.layout_puntajes)
        self.actualizar_salon_de_fama()
        self.show()

    def mensaje_desconexion(self):
        pop_mensaje_desconexion = QMessageBox()
        pop_mensaje_desconexion.setWindowTitle("Desconexión del servidor")
        pop_mensaje_desconexion.setText(f"""Se ha perdido la conexión con el servidor.""")
        pop_mensaje_desconexion.exec()
        self.salir()