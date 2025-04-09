from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtGui import QPixmap
import random
import parametros as p
from PyQt6.QtCore import QTimer


class Pepa(QObject):
    senal_actualizar_pixmap = pyqtSignal(list)
    senal_actualizar_label = pyqtSignal(int, int)
    senal_mover_label = pyqtSignal()

    def __init__(self, x: int, y: int, fila: int, columna: int) -> None:
        super().__init__()
        self.n = int()
        self.x = x
        self.y = y
        self.fila = fila
        self.columna = columna
        self.direcciones = {'up': (0, -25), 'down': (0, 25),
                            'left': (-25, 0), 'right': (25, 0)}
        self.crear_pixmaps()

    def crear_pixmaps(self):
        self.pepa_up = list()
        self.pepa_down = list()
        self.pepa_left = list()
        self.pepa_right = list()
        for i in range(4):
            pixmap_up = QPixmap(p.RUTA_PEPA_UP[i])
            pixmap_down = QPixmap(p.RUTA_PEPA_DOWN[i])
            pixmap_left = QPixmap(p.RUTA_PEPA_LEFT[i])
            pixmap_right = QPixmap(p.RUTA_PEPA_RIGHT[i])
            self.pepa_up.append(pixmap_up)
            self.pepa_down.append(pixmap_down)
            self.pepa_left.append(pixmap_left)
            self.pepa_right.append(pixmap_right)
        self.pixmap_direccion = {'up': self.pepa_up,
                                 'down': self.pepa_down,
                                 'left': self.pepa_left,
                                 'right': self.pepa_right}

    def mover_pepa(self, direccion):
        incremento = self.direcciones[direccion]
        self.senal_actualizar_pixmap.emit(self.pixmap_direccion[direccion])
        self.x += incremento[0]
        self.y += incremento[1]
        self.fila += incremento[1] // 25
        self.columna += incremento[0] // 25
        self.senal_actualizar_label.emit(int(self.x), int(self.y))
        self.senal_mover_label.emit()

    def reiniciar_pepa(self):
        self.x = 25
        self.y = 25
        self.fila = 0
        self.columna = 0
        self.crear_pixmaps()


class Sandia(QObject):
    id = 0
    def __init__(self) -> None:
        super().__init__()
        self.x = random.randint(0, 800)
        self.y = random.randint(0, 600)
        self.activa = False
        self.timer_desaparecer_sandia = QTimer()
        self.timer_desaparecer_sandia.setInterval(p.TIEMPO_DURACION * 1000)
        self.timer_desaparecer_sandia.timeout.connect(self.eliminar_sandia)
        self.id = Sandia.id
        Sandia.id += 1

    def activar_sandia(self):
        self.activa = True
        self.timer_desaparecer_sandia.start()

    def eliminar_sandia(self):
        self.timer_desaparecer_sandia.stop()
        self.activa = False