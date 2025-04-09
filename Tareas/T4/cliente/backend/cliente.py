from PyQt6.QtCore import pyqtSignal, QObject
import socket
import threading
import json
from backend.funciones_cliente import serializar, deserializar, codificar, decodificar

class Cliente(QObject):
    senal_mensaje_servidor = pyqtSignal(bool)
    senal_error_serivor = pyqtSignal()

    def __init__(self, port: int, host: str):
        super().__init__()
        self.chunk_size = 2**12
        self.port = port
        self.host = host
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conectado = False
        try:
            self.socket_cliente.connect((self.host, self.port))
            self.conectado = True
            self.listen()

        except (ConnectionError):
            self.senal_error_serivor.emit()
            self.socket_cliente.close()
            self.conectado = False
        
    def enviar_solucion(self, solucion: list, nombre_puzzle: str):
        solucion_json = serializar(solucion)
        mensaje_codificado = codificar(solucion_json, nombre_puzzle)
        self.socket_cliente.sendall(mensaje_codificado)

    def listen(self):
        thread = threading.Thread(target=self.listen_thread, daemon=True)
        thread.start()

    def listen_thread(self):
        try:
            while self.conectado:
                data = self.socket_cliente.recv(self.chunk_size)
                mensaje_decodificado = decodificar(bytearray(data))
                mensaje = deserializar(mensaje_decodificado)
                self.senal_mensaje_servidor.emit(mensaje)
        except ConnectionResetError:
            self.senal_error_serivor.emit()
            self.conectado = False
        finally:
            self.socket_cliente.close()