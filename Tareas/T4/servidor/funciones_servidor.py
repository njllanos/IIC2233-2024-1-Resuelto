import json
import os

def solucion_valida(solucion, nombre_puzzle):
    with open(os.path.join("servidor", "assets", "solucion_puzzles", nombre_puzzle), "r") as doc:
        lineas = doc.readlines()
    lista_puzzle = []
    for linea in lineas:
        linea = linea.strip("\n")
        lista_puzzle.append([int(x) for x in linea])
    return lista_puzzle == solucion


def codificar(mensaje_array):
    mensaje = bytearray(mensaje_array.encode())
    largo_codificado = len(mensaje).to_bytes(4, byteorder="big")
    array_codificado = bytearray(largo_codificado)
    for index in range(0, len(mensaje) // 25):
        numero_chunk = (index).to_bytes(3, byteorder="big")
        array_codificado.extend(numero_chunk)
        chunk = mensaje[index * 25: index * 25 + 25]
        array_codificado.extend(chunk)
    resto = mensaje[len(mensaje) - (len(mensaje) % 25):]
    while len(resto) < 25:
        resto.extend(bytes([0]))
    array_codificado.extend(resto)
    return array_codificado

def decodificar(mensaje_array: bytearray) -> bytearray:
    mensaje = mensaje_array.copy()
    array_decodificado = bytearray()
    largo_mensaje = int.from_bytes(mensaje[:4], byteorder='big')
    mensaje_sin_largo = mensaje[4:]
    for index in range(0, largo_mensaje // 25):
        inicio = index * 25 + (index + 1) * 3
        chunk = mensaje_sin_largo[inicio:inicio + 25]
        array_decodificado.extend(chunk)
    resto = mensaje_sin_largo[len(mensaje_sin_largo) - 25:]
    array_decodificado.extend(resto)
    return bytearray(array_decodificado[:largo_mensaje])

def serializar(mensaje):
    string_json = json.dumps(mensaje)
    return string_json

def deserializar(array):
    return json.loads(array)