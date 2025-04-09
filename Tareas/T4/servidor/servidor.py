import socket
import threading
import json
from funciones_servidor import codificar, decodificar, serializar, deserializar, solucion_valida

class Servidor:
    def __init__(self, port: int, host: str):
        self.chunk_size = 2**12
        self.host = host
        self.port = port
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind_listen()
        self.accept_connections()

    def bind_listen(self):
        self.socket_server.bind((self.host, self.port))
        self.socket_server.listen()
        print(f'''{'*** Servidor Conectado ***'.center(100)}''')

    def accept_connections(self) -> None:
        thread = threading.Thread(
            target=self.accept_connections_thread)
        thread.start()

    def accept_connections_thread(self):
        try:
            while True:
                socket_cliente, address = self.socket_server.accept()
                listening_client_thread = threading.Thread(
                    target=self.listen_client_thread,
                    args=(socket_cliente, ),
                    daemon=True)
                listening_client_thread.start()
                print("Se ha conectado un cliente")
        except ConnectionResetError:
                print("Desconexion del Servidor")
    
    def listen_client_thread(self, socket_cliente: socket) -> None:
        while True:
            try:
                bytes_mensaje = self.recibir_bytes(socket_cliente)
                mensaje_decodificado = decodificar(bytes_mensaje)
                mensaje_str = mensaje_decodificado.decode()
                solucion_str, nombre_puzzle = mensaje_str.split("|")
                solucion = deserializar(solucion_str)
                self.procesar_solucion(solucion, nombre_puzzle, socket_cliente)
            except ConnectionResetError:
                print("Cliente se ha desconectado, se ha descartado su conexion")
                socket_cliente.close()
                break

    def procesar_solucion(self, solucion, nombre_puzzle, socket_cliente) -> None:
        if solucion_valida(solucion, nombre_puzzle):
            mensaje = True
        else:
            mensaje = False
        self.enviar_mensaje(mensaje, socket_cliente)

    def enviar_mensaje(self, mensaje: str, socket_cliente: socket) -> None:
        mensaje_serializado = serializar(mensaje)
        mensaje_codificado = codificar(mensaje_serializado)
        socket_cliente.sendall(mensaje_codificado)

    def recibir_bytes(self, socket_cliente: socket) -> bytearray:
        bytes_leidos = bytearray()
        respuesta = socket_cliente.recv(self.chunk_size)
        bytes_leidos.extend(respuesta)
        return bytes_leidos