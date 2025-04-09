from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, 
                            QScrollArea, QPushButton, QMessageBox, QGridLayout, QFormLayout)
from PyQt6.QtGui import QFont, QPixmap, QMouseEvent, QKeyEvent
from PyQt6.QtCore import Qt, pyqtSignal, QObject, QTimer, QMutex
import parametros as p
from frontend.funciones_frontend import borrar_layout, limpiar_layout

class VentanaJuego(QWidget):
    senal_volver_inicio = pyqtSignal()
    senal_posicion_inicial_pepa = pyqtSignal(int, int)
    senal_tecla = pyqtSignal(str)
    senal_interacion_g = pyqtSignal(str)
    senal_sandia_clickeada = pyqtSignal(object)
    senal_pausa = pyqtSignal()
    senal_reanudar = pyqtSignal()
    senal_musica_fondo = pyqtSignal()
    senal_cheatcode_inf = pyqtSignal()
    senal_cheatcode_mute = pyqtSignal()
    senal_comprobar_puzzle = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timer_mover_pepa = False
        self.timer_animacion_pepa = False
        self.init_gui()

    def init_gui(self) -> None:
        self.setGeometry(50, 50, 800, 650)
        self.setFixedSize(800, 650)
        self.setWindowTitle("Ventana de Juego")
        self.layout_compilado = QHBoxLayout()
        self.layout_izquierda = QVBoxLayout()
        self.layout_puzzle = QGridLayout()
        self.layout_puzzle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_puzzle.setSpacing(0)
        self.layout_izquierda.addLayout(self.layout_puzzle)
        self.layout_derecha = QVBoxLayout()
        self.layout_derecha.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout_derecha.setSpacing(100)
        self.grilla_tiempo = QFormLayout()
        self.texto_tiempo = QLabel("Tiempo restante:")
        self.cronometro = QLabel("00:00")
        self.cronometro.setFont(QFont("Arial", 11))
        self.texto_tiempo.setFont(QFont("Arial", 11))
        self.grilla_tiempo.addRow(self.texto_tiempo, self.cronometro)
        self.grilla_tiempo.setSpacing(3)
        self.layout_derecha.addLayout(self.grilla_tiempo)
        self.boton_comprobar = QPushButton("Comprobar")
        self.boton_comprobar.setStyleSheet(f"""background-color: blue; border-style:
                        outset; border-width: 2px;border-radius: 10px; border-color: 
                        beige; font: bold 14px; min-width: 9em; padding: 6px;""")
        self.layout_derecha.addWidget(self.boton_comprobar)
        self.boton_comprobar.clicked.connect(self.comprobar_puzzle)
        self.boton_pausar = QPushButton("Pausar")
        self.boton_pausar.setStyleSheet(f"""background-color: yellow; border-style: 
                        outset; border-width: 2px;border-radius: 10px; border-color: 
                        beige; font: bold 14px; min-width: 9em; padding: 6px;""")
        self.layout_derecha.addWidget(self.boton_pausar)
        self.boton_pausar.clicked.connect(self.pausar)
        self.boton_salir = QPushButton("Salir")
        self.boton_salir.setStyleSheet(f"""background-color: red; border-style: outset; 
                        border-width: 2px;border-radius: 10px; border-color: beige; 
                        font: bold 14px; min-width: 9em; padding: 6px;""")
        self.layout_derecha.addWidget(self.boton_salir)
        self.boton_salir.clicked.connect(self.salir)
        self.layout_compilado.addLayout(self.layout_izquierda, 1)
        self.layout_compilado.addLayout(self.layout_derecha)
        self.setLayout(self.layout_compilado)

        self.imagen_actual_pepa = 0
        if not self.timer_mover_pepa:
            self.timer_mover_pepa = QTimer(self)
            self.timer_mover_pepa.setInterval(10)
            self.timer_mover_pepa.timeout.connect(self.mover_pepa)
        if not self.timer_animacion_pepa:
            self.timer_animacion_pepa = QTimer(self)
            self.timer_animacion_pepa.setInterval(30)
            self.timer_animacion_pepa.timeout.connect(self.cambiar_pixmap_pepa)
        self.pixmaps_pepa = list()
        self.label_pepa = QLabel(self)
        self.label_pepa.setFixedSize(25, 25)
        self.label_pepa.setPixmap(QPixmap(p.RUTA_PEPA_DOWN[0]))
        self.label_pepa.setScaledContents(True)
        self.visibilidad_pepa = False
        self.label_pepa.setVisible(self.visibilidad_pepa)

        self.flag_teclado = True
        self.puzzle_visible = True
        self.i_press = False
        self.n_press = False
        self.f_press = False
        self.m_press = False
        self.u_press = False
        self.t_press = False
        self.e_press = False

        self.dic_labels_sandias = {}
        self.sandias_historial = {}
        self.flag_mouse = True

    def adaptar_puzzle(self, n, columnas, filas):
        for i in range(len(columnas)):
            numeros = QLabel(str(columnas[i]))
            numeros.setFixedSize(25, 80)
            numeros.setFont(QFont("Arial", 10))
            numeros.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)
            estilo = "border: 1px solid gray; border-bottom: 2px solid black;"
            if i == 0:
                numeros.setStyleSheet(estilo + "border-left: 2px solid black; border-top: white")
            elif i == len(columnas) - 1:
                numeros.setStyleSheet(estilo + "border-right: 2px solid black; border-top: white")
            else:
                numeros.setStyleSheet(estilo + "border-top: white")
            self.layout_puzzle.addWidget(numeros, 0, i + 1)
        for j in range(len(filas)):
            numeros = QLabel(str(filas[j]))
            numeros.setFixedSize(80, 25)
            numeros.setFont(QFont("Arial", 10))
            numeros.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignRight)
            if j == 0:
                numeros.setStyleSheet(f"""border: 1px solid gray; border-top: 2px solid black; 
                                    border-right: 2px solid black; border-left: white""")
            elif j == len(filas) - 1:
                numeros.setStyleSheet(f"""border: 1px solid gray; border-bottom: 2px solid black; 
                                    border-right: 2px solid black; border-left: white""")
            else:
                numeros.setStyleSheet(f"""border: 1px solid gray; border-right: 2px solid black; 
                                    border-left: white""")
            self.layout_puzzle.addWidget(numeros, j + 1, 0)
        for i in range(n):
            for j in range(n):
                casilla = QLabel()
                casilla.setFixedSize(25, 25)
                casilla.setAlignment(Qt.AlignmentFlag.AlignCenter)
                estilo = "background-color: white; border: 1px solid gray;"
                if i == 0:
                    if j == n - 1:
                        casilla.setStyleSheet(estilo + f"""border-top: None; 
                                                    border-right: 2px solid black""")
                    else:
                        casilla.setStyleSheet(estilo + "border-top: None")
                elif j == n - 1:
                    if i == n - 1:
                        casilla.setStyleSheet(estilo + f"""border-right: 2px solid black; 
                                                    border-bottom: 2px solid black""")
                    else:
                        casilla.setStyleSheet(estilo + "border-right: 2px solid black")
                elif i == n - 1:
                    casilla.setStyleSheet(estilo + "border-bottom: 2px solid black")
                else:
                    casilla.setStyleSheet("background-color: white; border: 1px solid gray")
                self.layout_puzzle.addWidget(casilla, i + 1, j + 1)
                self.agregar_lechuga(i, j)
        self.setLayout(self.layout_compilado)  
        self.mostrar_ventana()

    def agregar_lechuga(self, fila, col):
        if self.layout_puzzle.itemAtPosition(fila + 1, col + 1) is not None:
            casilla = self.layout_puzzle.itemAtPosition(fila + 1, col + 1).widget()
            label_lechuga = QLabel()
            label_lechuga.setFixedSize(22, 22)
            label_lechuga.setStyleSheet("border: None; background-color: white")
            label_lechuga.setPixmap(QPixmap(p.RUTA_LECHUGA))
            label_lechuga.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label_lechuga.setScaledContents(True)
            if casilla.layout() is None:
                layout_lechuga = QVBoxLayout()
                layout_lechuga.setAlignment(Qt.AlignmentFlag.AlignCenter)
                layout_lechuga.setContentsMargins(0, 0, 0, 0)
                layout_lechuga.addWidget(label_lechuga)
                casilla.setLayout(layout_lechuga)
            else:
                limpiar_layout(casilla.layout())
                layout_lechuga = casilla.layout()
                layout_lechuga.addWidget(label_lechuga)
            self.levantar_label(label_lechuga)

    def aparecer_poop(self, fila, col):
        casilla = self.layout_puzzle.itemAtPosition(fila + 1, col + 1).widget()
        layout_poop = casilla.layout()
        label_poop = QLabel()
        label_poop.setFixedSize(20, 20)
        label_poop.setStyleSheet("border: None; background-color: white")
        label_poop.setPixmap(QPixmap(p.RUTA_POOP))
        label_poop.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_poop.setScaledContents(True)
        layout_poop.addWidget(label_poop)
        casilla.poop_label = label_poop
        self.levantar_label(label_poop)

    def quitar_lechuga(self, fila, col):
        casilla = self.layout_puzzle.itemAtPosition(fila + 1, col + 1).widget()
        limpiar_layout(casilla.layout())

    def mostrar_ventana(self):
        self.senal_musica_fondo.emit()
        self.show()

    def salir(self):
        self.close()

    def volver_a_inicio(self):
        for sandia_id in self.sandias_historial.keys():
            if self.sandias_historial[sandia_id].activa:
                self.dic_labels_sandias[sandia_id].setVisible(False)
                self.sandias_historial[sandia_id].eliminar_sandia()
        self.timer_mover_pepa.stop()
        self.timer_animacion_pepa.stop()
        self.label_pepa.setVisible(False)
        self.borrar_layouts_ventana()
        self.init_gui()
        self.salir()
        self.senal_volver_inicio.emit()

    def borrar_layouts_ventana(self):
        for layout in [self.layout_puzzle, self.layout_izquierda, 
                    self.layout_derecha, self.layout_compilado]:
            borrar_layout(layout)

    def aparecer_pepa(self, fila, col):
        self.pepa_fila = fila
        self.pepa_col = col
        x = self.layout_puzzle.itemAtPosition(fila + 1, col + 1).geometry().x()
        y = self.layout_puzzle.itemAtPosition(fila + 1, col + 1).geometry().y()
        self.pepa_x = x
        self.pepa_y = y
        self.senal_posicion_inicial_pepa.emit(x, y)
        self.label_pepa.move(x, y)
        self.visibilidad_pepa = True
        self.label_pepa.setVisible(self.visibilidad_pepa)
        self.levantar_label(self.label_pepa)

    def levantar_label(self, label):
        label.raise_()

    def pausar(self):
        self.puzzle_visible = not self.puzzle_visible
        self.flag_teclado = not self.flag_teclado
        self.flag_mouse = not self.flag_mouse
        self.visibilidad_pepa = not self.visibilidad_pepa
        self.label_pepa.setVisible(self.visibilidad_pepa)
        for i in range(self.layout_puzzle.count()):
            widget = self.layout_puzzle.itemAt(i).widget()
            if widget:
                widget.setVisible(self.puzzle_visible)
        if not self.puzzle_visible:
            self.timer_mover_pepa.stop()
            self.timer_animacion_pepa.stop()
            self.senal_pausa.emit()
            for sandia_id in self.sandias_historial.keys():
                if self.sandias_historial[sandia_id].activa:
                    self.dic_labels_sandias[sandia_id].setVisible(False)
        else:
            for sandia_id in self.sandias_historial.keys():
                if self.sandias_historial[sandia_id].activa:
                    self.dic_labels_sandias[sandia_id].setVisible(True)
            self.timer_mover_pepa.start()
            self.timer_animacion_pepa.start()
            self.senal_reanudar.emit()

    def keyPressEvent(self, event):
        if self.flag_teclado is True:
            if self.timer_mover_pepa.isActive() is False:
                if event.key() == Qt.Key.Key_A and not event.isAutoRepeat():
                    self.senal_tecla.emit('left')
                if event.key() == Qt.Key.Key_D and not event.isAutoRepeat():
                    self.senal_tecla.emit('right')
                if event.key() == Qt.Key.Key_W and not event.isAutoRepeat():
                    self.senal_tecla.emit('up')
                if event.key() == Qt.Key.Key_S and not event.isAutoRepeat():
                    self.senal_tecla.emit('down')
                if event.key() == Qt.Key.Key_G:
                    self.senal_interacion_g.emit('g')
                if event.key() == Qt.Key.Key_I:
                    self.i_press = True
                if event.key() == Qt.Key.Key_N:
                    self.n_press = True
                if event.key() == Qt.Key.Key_F:
                    self.f_press = True
                if event.key() == Qt.Key.Key_M:
                    self.m_press = True
                if event.key() == Qt.Key.Key_U:
                    self.u_press = True
                if event.key() == Qt.Key.Key_T:
                    self.t_press = True
                if event.key() == Qt.Key.Key_E:
                    self.e_press = True
                if self.i_press and self.n_press and self.f_press:
                    self.senal_cheatcode_inf.emit()
                if self.m_press and self.u_press and self.t_press and self.e_press:
                    self.senal_cheatcode_mute.emit()

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key.Key_I:
            self.i_press = False
        elif event.key() == Qt.Key.Key_N:
            self.n_press = False
        elif event.key() == Qt.Key.Key_F:
            self.f_press = False
        elif event.key() == Qt.Key.Key_M:
            self.m_press = False
        elif event.key() == Qt.Key.Key_U:
            self.u_press = False
        elif event.key() == Qt.Key.Key_T:
            self.t_press = False
        elif event.key() == Qt.Key.Key_E:
            self.e_press = False

    def mover_pepa(self):
        label_x = self.label_pepa.x()
        label_y = self.label_pepa.y()
        if self.pepa_x != label_x:
            if self.pepa_x < label_x:
                self.label_pepa.move(label_x - 1, label_y)
            elif self.pepa_x > label_x:
                self.label_pepa.move(label_x + 1, label_y)
        elif self.pepa_y != label_y:
            if self.pepa_y < label_y:
                self.label_pepa.move(label_x, label_y - 1)
            elif self.pepa_y > label_y:
                self.label_pepa.move(label_x, label_y + 1)
        else:
            self.label_pepa.setPixmap(QPixmap(p.RUTA_PEPA_DOWN[0]))
            self.timer_mover_pepa.stop()
            self.timer_animacion_pepa.stop()

    def actualizar_label_pepa(self, x, y):
        self.pepa_x = x
        self.pepa_y = y

    def cambiar_pixmap_pepa(self):
        if self.pixmaps_pepa:
            pixmap_nuevo = self.pixmaps_pepa[self.imagen_actual_pepa]
            self.label_pepa.setPixmap(pixmap_nuevo)
            self.imagen_actual_pepa += 1
            if self.imagen_actual_pepa >= len(self.pixmaps_pepa):
                self.imagen_actual_pepa = 0

    def lista_pixmap(self, lista_fotos):
        self.pixmaps_pepa = lista_fotos

    def aparecer_sandia(self, sandia, x, y):
        label_sandia = QLabel(self)
        label_sandia.setFixedSize(p.TAMAÑO_SANDIA, p.TAMAÑO_SANDIA)
        label_sandia.setPixmap(QPixmap(p.RUTA_SANDIA))
        label_sandia.setScaledContents(True)
        label_sandia.move(x, y)
        sandia.timer_desaparecer_sandia.timeout.connect(lambda: 
                                                        self.desaparecer_sandia(sandia, x, y))
        self.sandias_historial[sandia.id] = sandia
        self.dic_labels_sandias[sandia.id] = label_sandia
        self.dic_labels_sandias[sandia.id].setVisible(True)

    def mousePressEvent(self, event):
        if self.flag_mouse:
            for sandia in self.sandias_historial.values():
                if sandia.id in self.dic_labels_sandias and sandia.activa is True:
                    if self.dic_labels_sandias[sandia.id].geometry().contains(event.pos()):
                        self.senal_sandia_clickeada.emit(sandia)

    def desaparecer_sandia(self, sandia, x, y):
        if sandia.id in self.sandias_historial:
            self.dic_labels_sandias[sandia.id].setVisible(False)

    def actualizar_tiempo(self, tiempo: str):
        self.cronometro.setText(tiempo)

    def comprobar_puzzle(self):
        self.senal_comprobar_puzzle.emit()

    def mensaje_perder(self):
        pop_mensaje_perder = QMessageBox()
        pop_mensaje_perder.setWindowTitle("Fin del Juego: se ha acabado el tiempo")
        pop_mensaje_perder.setText(f"""Fin del juego, se ha acabado el tiempo.
¡Vuelve a intentarlo!""")
        pop_mensaje_perder.exec()
        self.volver_a_inicio()

    def mensaje_ganar(self, puntaje: float):
        pop_mensaje_ganar = QMessageBox()
        pop_mensaje_ganar.setWindowTitle("Fin del Juego: Puzzle completado")
        pop_mensaje_ganar.setText(f"Fin del juego, ¡Haz ganado!\nTu puntaje ha sido {puntaje}")
        pop_mensaje_ganar.exec()
        self.volver_a_inicio()

    def mensaje_solucion_erronea(self):
        pop_mensaje_erronea = QMessageBox()
        pop_mensaje_erronea.setWindowTitle("Solución incorrecta")
        pop_mensaje_erronea.setText(f"""La solución ingresada es incorrecta.
¡Sigue intentando!""")
        pop_mensaje_erronea.exec()
    
    def mensaje_desconexion(self):
        pop_mensaje_desconexion = QMessageBox()
        pop_mensaje_desconexion.setWindowTitle("Desconexión del servidor")
        pop_mensaje_desconexion.setText(f"""Se ha perdido la conexión con el servidor.
No se podrán corroborar los puzzles.""")
        pop_mensaje_desconexion.exec()
        self.salir()