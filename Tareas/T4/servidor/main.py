import os
import sys
import json
from funciones_servidor import codificar, decodificar, serializar, deserializar, solucion_valida
from servidor import Servidor


if __name__ == '__main__':
    def hook(type, value, traceback) -> None:
        print(type)
        print(traceback)
    
    sys.__excepthook__ = hook

    with open(os.path.join("servidor", "parametros.json"), "rb") as archivo_json:
        parametros = json.load(archivo_json)
    PORT = 3247 if len(sys.argv) < 2 else int(sys.argv[1])
    HOST = parametros["host"]
    server = Servidor(PORT, HOST)