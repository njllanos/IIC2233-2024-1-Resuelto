from functools import reduce

def calcular_edad(animal, diccionario):
    return animal.edad * diccionario[animal.especie].ponderador

def local_cumple_votos_min(local, cantidad_minima_votantes):
        return reduce(lambda x, y: x + 1, local.id_votantes, 0) >= cantidad_minima_votantes

def mismo_distrito(pareja):
        return pareja[0].id_distrito_postulacion == pareja[1].id_distrito_postulacion

def mismo_mes(animal, candidato):
        mismo_ano = animal.fecha_nacimiento[:4] == candidato[0].fecha_nacimiento[:4] 
        mismo_mes = animal.fecha_nacimiento[5:] == candidato[0].fecha_nacimiento[5:]
        return mismo_ano or mismo_mes

def bisiesto(animal):
        ano = int(animal.fecha_nacimiento[:4])
        if ano % 4 == 0 and (ano % 100 != 0 or ano % 400 == 0):
            return True
        else:
            return False

def empate(pareja, dict_candidato_votos):
        candidato_1 = pareja[0].id_candidato
        candidato_2 = pareja[1].id_candidato
        return dict_candidato_votos[candidato_1] == dict_candidato_votos[candidato_2]

def entre_edades(animal, animales_votantes, edad_minima, edad_maxima, ponderador):
        animal_votante = (animal.id in animales_votantes)
        if animal_votante:
            animal_entre_edades = (edad_minima <= animal.edad * ponderador[0] <= edad_maxima)
        return animal_votante and animal_entre_edades

def cumple_con_edad(animal, comparador, edad, dict_especie_ponderador):
        if comparador == "=":
            return calcular_edad(animal, dict_especie_ponderador) == edad
        if comparador == ">":
            return calcular_edad(animal, dict_especie_ponderador) > edad
        if comparador == "<":
            return calcular_edad(animal, dict_especie_ponderador) < edad

def filtrar_edad(generador_animales, edad, comparador):
    if comparador == ">":
       generador_animales = filter(lambda x: x.edad > edad, generador_animales)
    if comparador == "=":
       generador_animales = filter(lambda x: x.edad == edad, generador_animales)
    if comparador == "<":
       generador_animales = filter(lambda x: x.edad < edad, generador_animales)
    return generador_animales