import os
import parametros as p

def leer_puzzle(puzzle: str):
    ruta = os.path.join("cliente", "assets", "base_puzzles", puzzle)
    with open(ruta, "r") as archivo:
        columnas = archivo.readline().strip("\n").split(";")
        filas = archivo.readline().split(";")
    for i in range(len(columnas)):
        columnas[i] = columnas[i].replace(",", "\n")
    for j in range(len(filas)):
        filas[j] = filas[j].replace(",", "  ") + " "
    return len(columnas), columnas, filas

def segundos_a_string(segundos: int):
    decenas_minutos = round(segundos // 600, 0)
    minutos = round(segundos // 60, 0)
    segundos = round(segundos % 60, 0)
    if segundos < 10:
        segundos = f"0{segundos}"
    return f"{decenas_minutos}{minutos}:{segundos}"

def puzzle_a_binario(lista_puzzle):
    for i in range(len(lista_puzzle)):
        for j in range(len(lista_puzzle)):
            if lista_puzzle[i][j] == "L":
                lista_puzzle[i][j] = 1
            else:
                lista_puzzle[i][j] = 0
    return lista_puzzle

def escribir_puntajes(usuario: str, puntaje: float):
    with open(p.RUTA_PUNTAJE_TXT, 'a') as archivo:
        archivo.write(f"\n{usuario},{puntaje}")