from typing import List
from clases import Tortuga
import pickle


###################
#### ENCRIPTAR ####
###################
def serializar_tortuga(tortuga: Tortuga) -> bytearray:
    try:
        serializado = pickle.dumps(tortuga)
        byte = bytearray(serializado)
        return byte
    except AttributeError:
        raise ValueError("Error tipo ValueError")


def verificar_rango(mensaje: bytearray, inicio: int, fin: int) -> None:
    if (inicio < 0 or fin >= len(mensaje)):
        raise AttributeError()
    if not fin >= inicio:
        raise AttributeError()
    return None


def codificar_rango(inicio: int, fin: int) -> bytearray:
    start = (inicio).to_bytes(3, 'big')
    end = (fin).to_bytes(3, "big")
    byte = bytearray(start + end)
    return byte


def codificar_largo(largo: int) -> bytearray:
    large = (largo).to_bytes(3, "big")
    return bytearray(large)


def separar_msg(mensaje: bytearray, inicio: int, fin: int) -> List[bytearray]:
    m_extraido = bytearray()
    m_con_mascara = bytearray()
    if len(mensaje[inicio:fin + 1]) % 2 == 0:
        m_bytes_rango = mensaje[inicio:fin+1]
    elif len(mensaje[inicio:fin + 1]) % 2 != 0:
        m_bytes_rango = mensaje[inicio: fin + 1]
        m_bytes_rango = m_bytes_rango[::-1]
    contador = 0
    m_con_mascara = mensaje[:]
    for i in range(inicio, fin + 1):
        m_con_mascara[i] = contador
        contador += 1
    m_extraido = m_bytes_rango[:]
    return [m_extraido, m_con_mascara]


def encriptar(mensaje: bytearray, inicio: int, fin: int) -> bytearray:
    # No modificar
    verificar_rango(mensaje, inicio, fin)

    m_extraido, m_con_mascara = separar_msg(mensaje, inicio, fin)
    rango_codificado = codificar_rango(inicio, fin)
    return (
        codificar_largo(fin - inicio + 1)
        + m_extraido
        + m_con_mascara
        + rango_codificado
    )


######################
#### DESENCRIPTAR ####
######################
def deserializar_tortuga(mensaje_codificado: bytearray) -> Tortuga:
    try:
        deserializado = pickle.loads(mensaje_codificado)
        return deserializado
    except ValueError:
        raise AttributeError()


def decodificar_largo(mensaje: bytearray) -> int:
    primeros = mensaje[0:3]
    return int.from_bytes(primeros, byteorder='big')


def separar_msg_encriptado(mensaje: bytearray) -> List[bytearray]:
    m_extraido = bytearray()
    m_con_mascara = bytearray()
    rango_codificado = bytearray()
    largo = decodificar_largo(mensaje)
    rango_codificado.extend(mensaje[-6:])
    m_bytes_rango = mensaje[3: 3 + largo]
    m_con_mascara.extend(mensaje[3 + largo:-6])
    if len(m_bytes_rango) % 2 != 0:
        m_bytes_rango = m_bytes_rango[::-1]
    m_extraido.extend(m_bytes_rango)

    return [m_extraido, m_con_mascara, rango_codificado]


def decodificar_rango(rango_codificado: bytearray) -> List[int]:
    inicio = None
    fin = None
    inicio = int.from_bytes(rango_codificado[:3], "big")
    fin = int.from_bytes(rango_codificado[-3:], "big")

    return [inicio, fin]


def desencriptar(mensaje: bytearray) -> bytearray:
    largo = decodificar_largo(mensaje)
    m_bytes_rango, m_con_mascara, rango_codificado = separar_msg_encriptado(mensaje)
    inicio, fin = decodificar_rango(rango_codificado)
    contador = 0
    for i in range(inicio, fin + 1):
        m_con_mascara[i] = m_bytes_rango[contador]
        contador += 1
    return m_con_mascara


if __name__ == "__main__":
    # Tortuga
    tama = Tortuga("Tama2")
    print("Nombre: ", tama.nombre)
    print("Edad: ", tama.edad)
    print(tama.celebrar_anivesario())
    print()

    # Encriptar
    original = serializar_tortuga(tama)
    print("Original: ", original)
    encriptado = encriptar(original, 6, 24)
    print("Encriptado: ", encriptado)
    print()

    # Desencriptar
    mensaje =  bytearray(b'\x00\x00\x13roT\x07\x8c\x94sesalc\x06\x8c\x00\x00\x00\x00\x00\x80\x04\x958\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12tuga\x94\x93\x94)\x81\x94}\x94(\x8c\x06nombre\x94\x8c\x05Tama2\x94\x8c\x04edad\x94K\x01ub.\x00\x00\x06\x00\x00\x18')
    desencriptado = desencriptar(mensaje)
    tama = deserializar_tortuga(desencriptado)

    # Tortuga
    print("Tortuga: ", tama)
    print("Nombre: ", tama.nombre)
    print("Edad: ", tama.edad)
