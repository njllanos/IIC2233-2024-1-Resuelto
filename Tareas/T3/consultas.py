from typing import Generator
import os
from utilidades import (Animales, Candidatos, Distritos, Locales, Votos, Ponderador)
from functools import reduce
from itertools import combinations, product, tee, chain
from collections import Counter
from funciones import (calcular_edad, local_cumple_votos_min, mismo_distrito, 
                        mismo_mes, bisiesto, empate, entre_edades, cumple_con_edad, filtrar_edad)

# CARGA DE DATOS

def cargar_datos(tipo_generator: str, tamano: str):
    ruta = os.path.join("data", tamano, tipo_generator + ".csv")
    if os.path.exists(ruta):
        with open(ruta, "r") as archivo:
            archivo.readline()
            lineas = archivo.readlines()
            map_lineas = map(lambda x: x.strip().split(","), lineas)
            if tipo_generator == "animales":
                return map(lambda x: Animales(int(x[0]), x[1], x[2], int(x[3]), float(x[4]), 
                                                            int(x[5]), x[6]), map_lineas)
            if tipo_generator == "candidatos":
                return map(lambda x: Candidatos(int(x[0]), x[1], int(x[2]), x[3]), map_lineas)
            if tipo_generator == "distritos":
                return map(lambda x: Distritos(int(x[0]), x[1], int(x[2]), x[3], x[4]), map_lineas)
            if tipo_generator == "locales":
                return map(lambda x: Locales(int(x[0]), x[1], int(x[2]), 
                        [int(num.strip("[ ]")) for num in x[3:] if num.strip("[ ]")]), map_lineas)
            if tipo_generator == "ponderadores":
                return map(lambda x: Ponderador(x[0], float(x[1])), map_lineas)
            if tipo_generator == "votos":
                return map(lambda x: Votos(int(x[0]), int(x[1]), int(x[2]), int(x[3])), map_lineas)

# 1 GENERADOR

def animales_segun_edad(generador_animales: Generator,
    comparador: str, edad: int) -> Generator:
    generador_animales = filtrar_edad(generador_animales, edad, comparador)
    generador_nombres = map(lambda x: x.nombre, generador_animales)
    return generador_nombres


def animales_que_votaron_por(generador_votos: Generator,
    id_candidato: int) -> Generator:    
    generador_votos_filtrado = filter(lambda x: x.id_candidato == id_candidato, generador_votos)
    generador_id = map(lambda x: x.id_animal_votante, generador_votos_filtrado)
    return generador_id


def cantidad_votos_candidato(generador_votos: Generator,
    id_candidato: int) -> int:
    cuenta = reduce(lambda x, y: x + 1, animales_que_votaron_por(generador_votos, id_candidato), 0)
    return cuenta


def ciudades_distritos(generador_distritos: Generator) -> Generator:
    provincias = {distrito.provincia for distrito in generador_distritos}
    generador_provincias = (provincia for provincia in provincias)
    return generador_provincias


def especies_postulantes(generador_candidatos: Generator,
    postulantes: int) ->Generator:
    especies = [candidato.especie for candidato in generador_candidatos]
    especies_cumplen = [especie for especie in especies if especies.count(especie) >= postulantes]
    especies_cumplen_unicas = {especie for especie in especies_cumplen}
    generador_especies = (especie for especie in especies_cumplen_unicas)
    return generador_especies

def pares_candidatos(generador_candidatos: Generator) -> Generator:
    nombres = [candidato.nombre for candidato in generador_candidatos]
    combinaciones = combinations(nombres, 2)
    generador_combinaciones = (combinacion for combinacion in combinaciones)
    return generador_combinaciones


def votos_alcalde_en_local(generador_votos: Generator, candidato: int,
    local: int) -> Generator:
    votos_candidato = filter(lambda x: x.id_candidato == candidato, generador_votos)
    votos_local_candidato = filter(lambda x: x.id_local == local, votos_candidato)
    return votos_local_candidato


def locales_mas_votos_comuna(generador_locales: Generator,
    cantidad_minima_votantes: int, id_comuna: int) -> Generator:
    locales_comuna = [local for local in generador_locales if local.id_comuna == id_comuna]
    locales_que_cumplen = [local for local in locales_comuna if 
                                        local_cumple_votos_min(local, cantidad_minima_votantes)]
    generador_id_locales = [local.id_local for local in locales_que_cumplen]
    return generador_id_locales


def votos_candidato_mas_votado(generador_votos: Generator) -> Generator:
    votos = [voto for voto in generador_votos]
    id_candidato_votos = [voto.id_candidato for voto in votos]
    ids_ordenados_por_votacion = Counter(id_candidato_votos).most_common()
   
    max_votos = ids_ordenados_por_votacion[0][1]
    ids_mas_votados = [candidato[0] for candidato in ids_ordenados_por_votacion 
                                                    if candidato[1] >= max_votos]
    id_mas_votado = reduce(lambda x, y: x if x > y else y, ids_mas_votados)
    votos_candidato = [voto.id_voto for voto in votos if voto.id_candidato == id_mas_votado]
    return (voto for voto in votos_candidato)

# 2 GENERADORES

def animales_segun_edad_humana(generador_animales: Generator,
    generador_ponderadores: Generator, comparador: str,
    edad: int) -> Generator:
    animales = [animal for animal in generador_animales]
    especies = {animal.especie for animal in animales}
    pares_especie_ponderador = product((especie for especie in especies), generador_ponderadores)
    dict_especie_ponderador = {especie: ponderador for especie, ponderador in 
                                pares_especie_ponderador if ponderador.especie == especie}
    return (animal.nombre for animal in animales if 
                            cumple_con_edad(animal, comparador, edad, dict_especie_ponderador))


def animal_mas_viejo_edad_humana(generador_animales: Generator,
    generador_ponderadores: Generator) -> Generator:
    animales = [animal for animal in generador_animales]
    especies = {animal.especie for animal in animales}
    pares_especie_ponderador = product((especie for especie in especies), generador_ponderadores)
    dict_especie_ponderador = {especie: ponderador for especie, ponderador in 
                                    pares_especie_ponderador if ponderador.especie == especie}
    edades = (calcular_edad(animal, dict_especie_ponderador) 
                                                                        for animal in animales)
    edad_mayor = reduce(lambda x, y: x if x > y else y, edades)
    generador_nombres = (animal.nombre for animal in animales if 
                    calcular_edad(animal, dict_especie_ponderador) == edad_mayor)
    return generador_nombres


def votos_por_especie(generador_candidatos: Generator,
    generador_votos: Generator) -> Generator:
    dict_cadidato_especie = {candidato.id_candidato: candidato.especie 
                                                            for candidato in generador_candidatos}
    dict_voto = {voto.id_voto: voto.id_candidato for voto in generador_votos}
    votos_a_especies = [dict_cadidato_especie[dict_voto[id_voto]] for id_voto in dict_voto]
    dict_conteo_votos = Counter(votos_a_especies)
    especies = {especie for especie in dict_cadidato_especie.values()}
    dict_votos_por_especie = {especie: dict_conteo_votos.get(especie, 0) for especie in especies}
    return (especie_votos for especie_votos in dict_votos_por_especie.items())


def hallar_region(generador_distritos: Generator,
    generador_locales: Generator, id_animal: int) -> str:
    local_animal = filter(lambda x: id_animal in x.id_votantes, generador_locales)
    comuna_animal = next(local_animal).id_comuna
    distrito_animal = filter(lambda x: comuna_animal == x.id_comuna, generador_distritos)
    return next(distrito_animal).region


def max_locales_distrito(generador_distritos: Generator,
    generador_locales: Generator) -> Generator:
    dict_comuna_distrito = {distrito.id_comuna: distrito.nombre 
                                                            for distrito in generador_distritos}
    dict_local_comuna = {local.id_local: local.id_comuna for local in generador_locales}
    ids_comunas_locales = [dict_local_comuna[local] for local in dict_local_comuna]
    dict_comuna_locales = Counter(ids_comunas_locales)

    def contar_locales(distrito_nombre):
        return sum([dict_comuna_locales[comuna] for comuna in dict_comuna_distrito 
                                            if dict_comuna_distrito[comuna] == distrito_nombre])
    
    dict_distrito_locales = {distrito_nombre: contar_locales(distrito_nombre) 
                                            for distrito_nombre in dict_comuna_distrito.values()}
    max_locales = max(dict_distrito_locales.values())
    return (dist for dist in dict_distrito_locales if dict_distrito_locales[dist] == max_locales)


def votaron_por_si_mismos(generador_candidatos: Generator,
    generador_votos: Generator) -> Generator:
    voto_por_si_mismo = filter(lambda x: x.id_candidato == x.id_animal_votante, generador_votos)
    dict_candidatos = {candidato.id_candidato: candidato.nombre for 
                                                                candidato in generador_candidatos}
    return (dict_candidatos[voto.id_candidato] for voto in voto_por_si_mismo)


def ganadores_por_distrito(generador_candidatos: Generator,
    generador_votos: Generator) -> Generator:
    dict_voto_candidato = {voto.id_voto: voto.id_candidato for voto in generador_votos}
    ids_votos = (voto for voto in dict_voto_candidato.values())
    dict_candidato_votos = Counter(ids_votos)
    dict_candidato_distrito = {candidato: candidato.id_distrito_postulacion for 
                                                                candidato in generador_candidatos}
    candidatos = [candidato for candidato in dict_candidato_distrito]
    parejas = tee(combinations(candidatos, 2), 2)

    def ganador_pareja(pareja):
        return max(pareja, key= lambda x: dict_candidato_votos[x.id_candidato]).nombre

    ganadores = [ganador_pareja(pareja) for pareja in parejas[0] if mismo_distrito(pareja)]
    empates = [pareja[1].nombre for pareja in parejas[1] if 
                                mismo_distrito(pareja) and empate(pareja, dict_candidato_votos)]
    generador_union = (nombre for nombre in chain(ganadores, empates))
    return generador_union

# 3 o MAS GENERADORES

def mismo_mes_candidato(generador_animales: Generator,
    generador_candidatos: Generator, generador_votos: Generator,
    id_candidato: str) -> Generator:
    generadores_animales = tee(generador_animales, 2)
    votos_candidato = {voto.id_animal_votante for voto in generador_votos if 
                                                                voto.id_candidato == id_candidato}
    candidato = [animal for animal in generadores_animales[0] if animal.id == id_candidato]
    ids_que_cumplen = (animal.id for animal in generadores_animales[1] if 
                                (animal.id in votos_candidato) and mismo_mes(animal, candidato))
    return ids_que_cumplen
 

def edad_promedio_humana_voto_comuna(generador_animales: Generator,
    generador_ponderadores: Generator, generador_votos: Generator,
    id_candidato: int, id_comuna:int ) -> float:
    animales = [animal for animal in generador_animales]
    ids_votantes = [voto.id_animal_votante for voto in generador_votos if 
                                                                voto.id_candidato == id_candidato]
    ids_comuna = [animal.id for animal in animales if animal.id_comuna == id_comuna]
    ids_votantes_comuna = [id_animal for id_animal in ids_votantes if id_animal in ids_comuna]
    animales_votantes_comuna = [animal for animal in animales if animal.id in ids_votantes_comuna]
    if len(animales_votantes_comuna) == 0:
        return 0
    especies = {animal.especie for animal in animales_votantes_comuna}
    pares_especie_ponderador = product((especie for especie in especies), generador_ponderadores)
    dict_especie_ponderador = {especie: ponderador for especie, ponderador in 
                                        pares_especie_ponderador if ponderador.especie == especie}
    edades_ponderadas = [calcular_edad(animal, dict_especie_ponderador) for 
                                                            animal in animales_votantes_comuna]
    return sum(edades_ponderadas) / len(animales_votantes_comuna)


def votos_interespecie(generador_animales: Generator,
    generador_votos: Generator, generador_candidatos: Generator,
    misma_especie: bool = False) -> Generator:
    animales = [animal for animal in generador_animales]
    dict_id_especie = {animal.id: animal.especie for animal in animales}
    dict_id_voto = {voto.id_animal_votante: voto.id_candidato for voto in generador_votos}
    if misma_especie:
        ids_cumplen = [id_votante for id_votante in dict_id_voto if 
                        dict_id_especie[id_votante] == dict_id_especie[dict_id_voto[id_votante]]]
    else:
        ids_cumplen = [id_votante for id_votante in dict_id_voto if 
                        dict_id_especie[id_votante] != dict_id_especie[dict_id_voto[id_votante]]]
    dict_id_animal = {animal.id: animal for animal in animales}
    return (dict_id_animal[ids] for ids in ids_cumplen)


def porcentaje_apoyo_especie(generador_animales: Generator,
    generador_candidatos: Generator, generador_votos: Generator) -> Generator:
    generadores_votos = tee(generador_votos, 2)
    generadores_candidatos = tee(generador_candidatos, 2)
    dict_id_especie = {animal.id: animal.especie for animal in generador_animales}
    dict_candidato_especie = {candidato.id_candidato: candidato.especie for 
                                                        candidato in generadores_candidatos[0]}
    votos_por_especie = Counter([dict_id_especie[voto.id_animal_votante] for 
                                                        voto in generadores_votos[0]])
    
    def verificar(voto):
        candidato_valido = voto.id_candidato in dict_candidato_especie.keys()
        if candidato_valido:
            especie_candidato = dict_candidato_especie[voto.id_candidato]
            especie_votante = dict_id_especie[voto.id_animal_votante]
            misma_especie = (especie_candidato == especie_votante)
        return candidato_valido and misma_especie

    votos_candidato_apoyo = [voto.id_candidato for voto in generadores_votos[1] if verificar(voto)]
    votos_candidato_apoyo_conteo = Counter(votos_candidato_apoyo)

    def porcentaje_apoyo(candidato, votos_por_especie, votos_candidato_apoyo_conteo):
        especie = dict_candidato_especie[candidato.id_candidato]
        votos_especie = votos_por_especie[especie]
        votos_apoyo = votos_candidato_apoyo_conteo[candidato.id_candidato]
        if (votos_apoyo or votos_especie) == 0:
            return 0
        else:
            return round(100 * votos_apoyo / votos_especie, 0)

    dict_candidato_apoyo = {candidato.id_candidato: 
                    porcentaje_apoyo(candidato, votos_por_especie, votos_candidato_apoyo_conteo) 
                    for candidato in generadores_candidatos[1]}
    return (candidato_porcentaje for candidato_porcentaje in dict_candidato_apoyo.items())


def votos_validos(generador_animales: Generator,
    generador_votos: Generator, generador_ponderadores) -> int:
    generadores_animales = tee(generador_animales, 2)
    animales_votantes = {voto.id_animal_votante for voto in generador_votos}
    especies = {animal.especie for animal in generadores_animales[0]}
    pares_especie_ponderador = product((especie for especie in especies), generador_ponderadores)
    dict_especie_ponderador = {especie: ponderador for especie, ponderador in 
                                        pares_especie_ponderador if ponderador.especie == especie}
    edades_ponderadas = (calcular_edad(animal, dict_especie_ponderador) 
                        for animal in generadores_animales[1] if animal.id in animales_votantes)
    edades_validas = (edad for edad in edades_ponderadas if edad >= 18)
    return reduce(lambda x, y: x + 1, edades_validas, 0)


def cantidad_votos_especie_entre_edades(generador_animales: Generator,
    generador_votos: Generator, generador_ponderador: Generator,
    especie: str, edad_minima: int, edad_maxima: int) -> str:
    generadores_animales = tee(generador_animales, 2)
    dict_id_especie = {animal.id: animal.especie for animal in generadores_animales[0]}
    animales_votantes = {voto.id_animal_votante for voto in generador_votos if 
                                            dict_id_especie[voto.id_animal_votante] == especie}
    ponderador = [ponderador.ponderador for ponderador in generador_ponderador if 
                                                                    ponderador.especie == especie]
    animales = [animal for animal in generadores_animales[1] if 
                    entre_edades(animal, animales_votantes, edad_minima, edad_maxima, ponderador)]
    cantidad_votos = len(animales)
    mensaje_1 = f"Hubo {cantidad_votos} votos emitidos por animales entre {edad_minima} y"
    mensaje_2 = f" {edad_maxima} años de la especie {especie}."
    return mensaje_1 + mensaje_2


def distrito_mas_votos_especie_bisiesto(generador_animales: Generator,
    generador_votos: Generator, generador_distritos: Generator,
    especie: str) -> str:
    generadores_distritos = tee(generador_distritos, 2)
    generadores_animales = tee(generador_animales, 2)
    animales_bicestos_especie = {animal.id for animal in generadores_animales[0] if 
                                                bisiesto(animal) and animal.especie == especie}
    animales_votaron = {voto.id_animal_votante for voto in generador_votos}
    ids_que_cumplen = {ids for ids in animales_bicestos_especie if ids in animales_votaron}
    comunas = {animal.id_comuna for animal in generadores_animales[1] if 
                                                                    animal.id in ids_que_cumplen}
    dicionario_comuna_distrito = {distrito.id_comuna: distrito for 
                            distrito in generadores_distritos[0] if distrito.id_comuna in comunas}
    distritos = Counter([dicionario_comuna_distrito[comuna].nombre for comuna in comunas])
    if len(ids_que_cumplen) == 0:
        votos_max = 0
    else:
        votos_max = max(distritos.values())
    distritos_votos_max = [distrito for distrito in generadores_distritos[1] if 
                                                        distritos[distrito.nombre] == votos_max]
    distrito = min(distritos_votos_max, key=lambda x: x.id_distrito)
    mensaje_1 = f"El distrito {distrito.id_distrito} fue el que tuvo más votos emitidos por"
    mensaje_2 = f" animales de la especie {especie} nacidos en año bisiesto."
    return mensaje_1 + mensaje_2


def votos_validos_local(generador_animales: Generator,
    generador_votos: Generator, generador_ponderadores: Generator,
    id_local: int) -> Generator:
    generadores_animales = tee(generador_animales, 2)
    dict_id_voto = {voto.id_animal_votante: voto.id_voto for voto in generador_votos if 
                                                                        voto.id_local == id_local}
    especies = {animal.especie for animal in generadores_animales[0]}
    pares_especie_ponderador = product((especie for especie in especies), generador_ponderadores)
    dict_especie_ponderador = {especie: ponderador for especie, ponderador in 
                                        pares_especie_ponderador if ponderador.especie == especie}
    votos_validos = (dict_id_voto[animal.id] for animal in generadores_animales[1] if 
                calcular_edad(animal, dict_especie_ponderador) >= 18 and animal.id in dict_id_voto)
    return votos_validos


def votantes_validos_por_distritos(generador_animales: Generator,
    generador_distritos: Generator, generador_locales: Generator,
    generador_votos: Generator, generador_ponderadores: Generator) -> Generator:
    generadores_distritos = tee(generador_distritos, 3)
    generadores_animales = tee(generador_animales, 3)
    generadores_votos = tee(generador_votos, 3)
    generadores_locales = tee(generador_locales, 2)
    especies = {animal.especie for animal in generadores_animales[0]}
    pares_especie_ponderador = product((especie for especie in especies), generador_ponderadores)
    dict_especie_ponderador = {especie: ponderador for especie, ponderador in 
                                        pares_especie_ponderador if ponderador.especie == especie}
    dict_id_local = {voto.id_animal_votante: voto.id_local for voto in generadores_votos[0]}
    dict_local_local = {local.id_local: local for local in generadores_locales[0]}
    animales_validos = {animal for animal in generadores_animales[1] if 
                                            calcular_edad(animal, dict_especie_ponderador) >= 18}
    ids_votaron = {voto.id_animal_votante for voto in generadores_votos[1]}
    animales_que_cumplen_ids = {animal.id for animal in animales_validos 
                                        if animal.id in ids_votaron 
                                        and animal in animales_validos}
    comunas = [dict_local_local[dict_id_local[voto.id_animal_votante]].id_comuna for 
                voto in generadores_votos[2] if voto.id_animal_votante in animales_que_cumplen_ids]
    dicionario_comuna_distrito = {distrito.id_comuna: distrito for distrito in 
                                        generadores_distritos[0] if distrito.id_comuna in comunas}
    distritos = Counter([dicionario_comuna_distrito[comuna].nombre for comuna in comunas])
    if len(animales_que_cumplen_ids) == 0:
        votos_max = 0
    else:
        votos_max = max(distritos.values())
    distrito_ganador = min([distrito for distrito in generadores_distritos[1] if 
                            distritos[distrito.nombre] == votos_max], key=lambda x: x.id_distrito)
    comunas = {distrito.id_comuna for distrito in generadores_distritos[2] if 
                                                    distrito.nombre == distrito_ganador.nombre}
    locales = {local.id_local for local in generadores_locales[1] if local.id_comuna in comunas}
    animales = (animal for animal in generadores_animales[2] if 
                                                            dict_id_local[animal.id] in locales)
    return animales