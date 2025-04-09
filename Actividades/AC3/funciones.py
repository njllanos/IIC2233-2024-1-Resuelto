from copy import copy
from collections import defaultdict
from functools import reduce
from itertools import product
from typing import Generator
import os

from parametros import RUTA_PELICULAS, RUTA_GENEROS
from utilidades import (
    Pelicula, Genero, obtener_unicos, imprimir_peliculas,
    imprimir_generos, imprimir_peliculas_genero, imprimir_dccmax
)


# ----------------------------------------------------------------------------
# Parte 1: Cargar dataset
# ----------------------------------------------------------------------------

def cargar_peliculas(ruta: str) -> Generator:
    if os.path.exists(ruta):
        lista_peliculas = []
        with open(ruta, "r") as archivo:
            archivo.readline()  # leer primera linea
            for linea in archivo:
                datos = linea.strip().split(",")
                for i in range(len(datos)):
                    if datos[i].isnumeric():
                        datos[i] = int(datos[i])
                    if i == len(datos) - 1:
                        datos[i] = float(datos[i])
                lista_peliculas.append(Pelicula(*datos))
        for pelicula in lista_peliculas:
            yield pelicula


def cargar_generos(ruta: str) -> Generator:
    if os.path.exists(ruta):
        lista_generos = []
        with open(ruta, "r") as archivo:
            archivo.readline()  # leer primera linea
            for linea in archivo:
                datos = linea.strip().split(",")
                datos[1] = int(datos[1])
                lista_generos.append(Genero(*datos))
        for genero in lista_generos:
            yield genero


# ----------------------------------------------------------------------------
# Parte 2: Consultas sobre generadores
# ----------------------------------------------------------------------------

def obtener_directores(generador_peliculas: Generator) -> set:
    unicos = obtener_unicos(generador_peliculas)
    map_directores = map(lambda x: x.director, unicos)
    return obtener_unicos(map_directores)


def obtener_str_titulos(generador_peliculas: Generator) -> str:
    map_titulos = map(lambda x: x.titulo, generador_peliculas)
    string_titulos = ", ".join(map_titulos)
    return string_titulos


def filtrar_peliculas(
    generador_peliculas: Generator,
    director: str | None = None,
    rating_min: float | None = None,
    rating_max: float | None = None
) -> filter:
    if director is not None:
        generador_peliculas = filter(
            lambda x: x.director == director, generador_peliculas)
    if rating_min is not None:
        generador_peliculas = filter(
            lambda x: x.rating >= rating_min, generador_peliculas)
    if rating_max is not None:
        generador_peliculas = filter(
            lambda x: x.rating <= rating_max, generador_peliculas)
    return generador_peliculas


def filtrar_peliculas_por_genero(
    generador_peliculas: Generator,
    generador_generos: Generator,
    genero: str | None = None
) -> Generator:
    iterable = product(generador_peliculas, generador_generos)
    if genero is not None:
        filtrado = filter(
            lambda x: x[0].id_pelicula == x[1].id_pelicula and x[1].genero == genero, iterable)
    else:
        filtrado = filter(
            lambda x: x[0].id_pelicula == x[1].id_pelicula, iterable)
    return filtrado


# ----------------------------------------------------------------------------
# Parte 3: Iterables
# ----------------------------------------------------------------------------

class DCCMax:
    def __init__(self, peliculas: list) -> None:
        self.peliculas = peliculas

    def __iter__(self):
        return IteradorDCCMax(self.peliculas)


class IteradorDCCMax:
    def __init__(self, iterable_peliculas: list) -> None:
        self.peliculas = copy(iterable_peliculas)
        peliculas_ordenadas = sorted(self.peliculas, key=lambda x: (x.estreno, - x.rating))
        self.peliculas = peliculas_ordenadas

    def __iter__(self):
        return self

    def __next__(self) -> tuple:
        # Se levanta la excepción correspondiente
        if len(self.peliculas) == 0:
            raise StopIteration()

        siguiente = self.peliculas.pop(0)
        return siguiente


if __name__ == '__main__':
    print('> Cargar películas:')
    imprimir_peliculas(cargar_peliculas(RUTA_PELICULAS))
    print()

    print('> Cargar géneros')
    imprimir_generos(cargar_generos(RUTA_GENEROS), 5)
    print()

    print('> Obtener directores:')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    print(list(obtener_directores(generador_peliculas)))
    print()

    print('> Obtener string títulos')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    print(obtener_str_titulos(generador_peliculas))
    print()

    print('> Filtrar películas (por director):')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    imprimir_peliculas(filtrar_peliculas(
        generador_peliculas, director='Christopher Nolan'
    ))
    print('\n> Filtrar películas (rating min):')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    imprimir_peliculas(filtrar_peliculas(generador_peliculas, rating_min=9.1))
    print('\n> Filtrar películas (rating max):')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    imprimir_peliculas(filtrar_peliculas(generador_peliculas, rating_max=8.7))
    print()

    print('> Filtrar películas por género')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    generador_generos = cargar_generos(RUTA_GENEROS)
    imprimir_peliculas_genero(filtrar_peliculas_por_genero(
        generador_peliculas, generador_generos, 'Biography'
    ))
    print()

    print('> DCC Max...')
    imprimir_dccmax(DCCMax(list(cargar_peliculas(RUTA_PELICULAS))))
