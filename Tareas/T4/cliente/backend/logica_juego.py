from PyQt6.QtCore import pyqtSignal, QObject, QTimer, QUrl, QMutex
from backend.funciones_juego import (leer_puzzle, segundos_a_string, 
                                    puzzle_a_binario, escribir_puntajes)
from backend.entidades import Pepa, Sandia
import parametros as p
from PyQt6.QtMultimedia import QSoundEffect
import copy

class VentanaJuegoBackend(QObject):
    senal_adaptar_puzzle = pyqtSignal(int, list, list)
    senal_mostrar_pepa = pyqtSignal(int, int)
    senal_aparecer_lechuga = pyqtSignal(int, int)
    senal_aparecer_poop = pyqtSignal(int, int)
    senal_desaparecer_lechuga = pyqtSignal(int, int)
    senal_mostrar_sandia = pyqtSignal(object, int, int)
    senal_desaparecer_sandia = pyqtSignal(object, int, int)
    senal_actualizar_tiempo = pyqtSignal(str)
    senal_perder_pop = pyqtSignal()
    senal_enviar_solucion = pyqtSignal(list, str)
    senal_ganar_pop = pyqtSignal(float)
    senal_solucion_erronea = pyqtSignal()
    senal_mensaje_desconexion_pop = pyqtSignal()
    senal_cerrar_ventana = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.direcciones = {'up': (-1, 0), 'down': (1, 0),
                            'left': (0, -1), 'right': (0, 1)}
        self.crear_pepa()
        self.reproductor_efectos = QSoundEffect(self)
        self.reproductor_musica = QSoundEffect(self)
        self.mutex_puzzle_actual = QMutex()
        self.mutex_segundos_restantes = QMutex()
        self.timer_juego = False

    def comenzar(self, usuario: str, puzzle: str):
        self.mute_activado = False
        self.reproductor_efectos.setMuted(self.mute_activado)
        self.reproductor_musica.setMuted(self.mute_activado)

        self.timer_tiempo_utilizado = QTimer(self)
        self.timer_tiempo_utilizado.setInterval(1000)
        self.timer_tiempo_utilizado.timeout.connect(self.aumentar_tiempo)
        self.segundos_utilizados = 0

        self.timer_juego = QTimer(self)
        self.timer_juego.setInterval(1000)
        self.timer_juego.timeout.connect(self.disminuir_tiempo)
        self.mutex_segundos_restantes.lock()
        self.segundos_restantes = p.TIEMPO_JUEGO
        self.mutex_segundos_restantes.unlock()

        self.archivo_puzzle = puzzle
        self.nombre_usuario = usuario
        self.n, self.columnas, self.filas = leer_puzzle(self.archivo_puzzle)
        self.senal_adaptar_puzzle.emit(self.n, self.columnas, self.filas)
        self.mutex_puzzle_actual.lock()
        self.puzzle_actual = [["L" for i in range(self.n)] for j in range(self.n)]
        self.mutex_puzzle_actual.unlock()
        self.mutex_segundos_restantes.lock()
        self.senal_actualizar_tiempo.emit(segundos_a_string(self.segundos_restantes))
        self.mutex_segundos_restantes.unlock()
        self.pepa.n = self.n
        self.pepa.fila = 0
        self.pepa.columna = 0
        self.dic_timers_poop = {}
        self.inf_activado = False
        self.dic_tiempos_rest_poop = {}
        self.senal_mostrar_pepa.emit(0, 0)
        self.dic_sandias_activas = {}
        self.dic_time_rest_sandias = {}
        self.comenzar_timer_sandia()
        self.timer_juego.start()
        self.timer_tiempo_utilizado.start()

    def revisar_colisiones_pepa(self, direccion):
        fila_actual = self.pepa.fila
        columna_actual = self.pepa.columna
        fila_nueva = fila_actual + self.direcciones[direccion][0]
        columna_nueva = columna_actual + self.direcciones[direccion][1]
        if 1 <= fila_nueva + 1 <= self.n and 1 <= columna_nueva + 1 <= self.n:
            self.pepa.mover_pepa(direccion)
    
    def interaccion_g(self):
        fila_actual = self.pepa.fila
        columna_actual = self.pepa.columna
        self.mutex_puzzle_actual.lock()
        if self.puzzle_actual[fila_actual][columna_actual] == "L":
            self.puzzle_actual[fila_actual][columna_actual] = "V"
            file_url = QUrl.fromLocalFile(p.RUTA_COMER_WAV)
            self.reproductor_efectos.setSource(file_url)
            self.reproductor_efectos.play()
            self.senal_desaparecer_lechuga.emit(fila_actual, columna_actual)
        elif self.puzzle_actual[fila_actual][columna_actual] == "V":
            self.puzzle_actual[fila_actual][columna_actual] = "P"
            file_url = QUrl.fromLocalFile(p.RUTA_POOP_WAV)
            self.reproductor_efectos.setSource(file_url)
            self.reproductor_efectos.play()
            self.senal_aparecer_poop.emit(fila_actual, columna_actual)
            self.comenzar_timer_convertir_poop(fila_actual, columna_actual)
        self.mutex_puzzle_actual.unlock()

    def comenzar_timer_convertir_poop(self, fila, columna):
        timer_convertir_poop = QTimer(self)
        timer_convertir_poop.setSingleShot(True)
        timer_convertir_poop.timeout.connect(lambda: self.convertir_poop_a_lechuga(fila, columna))
        timer_convertir_poop.start(p.TIEMPO_CONVERSION_POOP * 1000)
        self.dic_timers_poop[(fila, columna)] = timer_convertir_poop

    def comenzar_timer_sandia(self):
        self.timer_crear_sandia = QTimer(self)
        self.timer_crear_sandia.setInterval(p.TIEMPO_APARICION * 1000)
        self.timer_crear_sandia.timeout.connect(self.crear_sandia)
        self.timer_crear_sandia.start()

    def convertir_poop_a_lechuga(self, fila, columna):
        self.puzzle_actual[fila][columna] = "L"
        self.senal_aparecer_lechuga.emit(fila, columna)

    def crear_pepa(self) -> None:
        self.pepa = Pepa(25, 25, 0, 0)

    def crear_sandia(self):
        sandia = Sandia()
        sandia.activar_sandia()
        self.dic_sandias_activas[sandia.id] = sandia
        self.senal_mostrar_sandia.emit(sandia, sandia.x, sandia.y)
        
    def posicion_inicial_pepa(self, x, y):
        self.pepa.x = x
        self.pepa.y = y

    def sandia_clickeada(self, sandia):
        if sandia.activa:
            file_url = QUrl.fromLocalFile(p.RUTA_OBTENER_SANDIA_WAV)
            self.reproductor_efectos.setSource(file_url)
            self.reproductor_efectos.play()
            self.mutex_segundos_restantes.lock()
            if self.inf_activado == False:
                self.segundos_restantes += p.TIEMPO_ADICIONAL
                self.senal_actualizar_tiempo.emit(segundos_a_string(self.segundos_restantes))
            self.mutex_segundos_restantes.unlock()
            self.desaparecer_sandia(sandia)
            sandia.eliminar_sandia()

    def desaparecer_sandia(self, sandia):
        if sandia.id in self.dic_sandias_activas:
            self.dic_sandias_activas.pop(sandia.id)
            self.senal_desaparecer_sandia.emit(sandia, sandia.x, sandia.y)

    def disminuir_tiempo(self):
        self.mutex_segundos_restantes.lock()
        self.segundos_restantes -= 1
        tiempo_restante_str = segundos_a_string(self.segundos_restantes)
        self.senal_actualizar_tiempo.emit(tiempo_restante_str)
        self.mutex_segundos_restantes.unlock()
        if self.segundos_restantes == 0:
            self.terminar_juego()
            self.perder()

    def terminar_juego(self):
        if self.timer_juego:
            self.timer_juego.stop()
            self.timer_tiempo_utilizado.stop()
            self.timer_crear_sandia.stop()
            self.pepa.reiniciar_pepa()
            for llave in self.dic_timers_poop.keys():
                if self.dic_timers_poop[llave] is not None:
                    self.dic_tiempos_rest_poop[llave] = self.dic_timers_poop[llave].remainingTime()
                    self.dic_timers_poop[llave].stop()
            for i in self.dic_sandias_activas.values():
                self.dic_time_rest_sandias[i.id] = i.timer_desaparecer_sandia.remainingTime()
                i.timer_desaparecer_sandia.stop()
            self.reproductor_musica.stop()

    def aumentar_tiempo(self):
        self.segundos_utilizados += 1

    def pausar_juego(self):
        self.timer_juego.stop()
        self.timer_tiempo_utilizado.stop()
        self.timer_crear_sandia.stop()
        for sandia in self.dic_sandias_activas.values():
            self.dic_time_rest_sandias[sandia.id] = sandia.timer_desaparecer_sandia.remainingTime()
            sandia.timer_desaparecer_sandia.stop()
        for llave in self.dic_timers_poop.keys():
            if self.dic_timers_poop[llave] is not None:
                self.dic_tiempos_rest_poop[llave] = self.dic_timers_poop[llave].remainingTime()
                self.dic_timers_poop[llave].stop()
    
    def reanudar(self):
        self.timer_crear_sandia.start()
        self.timer_juego.start()
        self.timer_tiempo_utilizado.start()
        for sandia in self.dic_sandias_activas.values():
            if self.dic_time_rest_sandias[sandia.id] >= 0:
                sandia.timer_desaparecer_sandia.start(self.dic_time_rest_sandias[sandia.id])
        for llave in self.dic_timers_poop.keys():
            if self.dic_timers_poop[llave] is not None and self.dic_tiempos_rest_poop[llave] >= 0:
                self.dic_timers_poop[llave].start(self.dic_tiempos_rest_poop[llave])

    def perder(self):
        file_url = QUrl.fromLocalFile(p.RUTA_JUEGO_PERDIDO_WAV)
        self.reproductor_efectos.setSource(file_url)
        self.reproductor_efectos.play()
        self.senal_perder_pop.emit()

    def ganar(self, puntaje):
        file_url = QUrl.fromLocalFile(p.RUTA_JUEGO_GANADO_WAV)
        self.reproductor_efectos.setSource(file_url)
        self.reproductor_efectos.play()
        self.senal_ganar_pop.emit(puntaje)

    def administar_musica_fondo(self):
        if self.reproductor_musica.isPlaying():
            self.reproductor_musica.stop()
        else:
            file_url = QUrl.fromLocalFile(p.RUTA_MUSICA_1_WAV)
            self.reproductor_musica.setSource(file_url)
            self.reproductor_musica.setLoopCount(-2)
            self.reproductor_musica.play()

    def cheatcode_inf(self):
        if self.inf_activado == False:
            self.inf_activado = True
            self.timer_juego.stop()
            self.senal_actualizar_tiempo.emit(str('INFINITO'))

    def cheatcode_mute(self):
        if self.mute_activado == False:
            self.mute_activado = True
            self.reproductor_efectos.setMuted(True)
            self.reproductor_musica.setMuted(True)

    def calcular_puntaje(self):
        if self.inf_activado:
            puntaje = p.PUNTAJE_INF
        else:
            puntaje_numinador = self.segundos_restantes * self.n *self.n * p.CONSTANTE
            puntaje_denominador = self.segundos_utilizados
            puntaje = round(puntaje_numinador / puntaje_denominador, 2)
        return puntaje

    def enviar_solucion(self):
        self.mutex_puzzle_actual.lock()
        puzzle_solucion = copy.deepcopy(self.puzzle_actual)
        self.mutex_puzzle_actual.unlock()
        solucion = puzzle_a_binario(puzzle_solucion)
        nombre_puzzle = self.archivo_puzzle
        self.senal_enviar_solucion.emit(solucion, nombre_puzzle)

    def mensaje_servidor(self, mensaje: bool):
        if mensaje is True:
            puntaje = self.calcular_puntaje()
            escribir_puntajes(self.nombre_usuario, puntaje)
            self.terminar_juego()
            self.ganar(puntaje)
        else:
            self.senal_solucion_erronea.emit()

    def error_servidor(self):
        self.terminar_juego()
        self.senal_mensaje_desconexion_pop.emit()
        self.senal_cerrar_ventana.emit()