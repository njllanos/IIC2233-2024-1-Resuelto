from abc import ABC, abstractmethod
import parametros
import random


class Combatiente(ABC):
    def __init__(self, nombre, vida_maxima, poder, defensa, agilidad,
                 resistencia) -> None:
        self.nombre = nombre
        self._vida_maxima = vida_maxima
        self._vida = vida_maxima
        self._poder = poder
        self._defensa = defensa
        self._agilidad = agilidad
        self._resistencia = resistencia

    @property
    def vida_maxima(self) -> int:
        return self._vida_maxima

    @vida_maxima.setter
    def vida_maxima(self, nueva_vida_maxima):
        if nueva_vida_maxima < parametros.MIN_VIDA:
            self._vida_maxima = parametros.MIN_VIDA
        elif nueva_vida_maxima > parametros.MAX_VIDA:
            self._vida_maxima = parametros.MAX_VIDA
        else:
            self._vida_maxima = nueva_vida_maxima

    @property
    def vida(self) -> int:
        return self._vida

    @vida.setter
    def vida(self, nueva_vida):
        if nueva_vida < parametros.MIN_VIDA:
            self._vida = parametros.MIN_VIDA
        elif nueva_vida > self.vida_maxima:
            self._vida = self.vida_maxima
        else:
            self._vida = nueva_vida

    @property
    def poder(self) -> int:
        return self._poder

    @poder.setter
    def poder(self, nuevo_poder):
        if nuevo_poder < parametros.MIN_PODER:
            self._poder = parametros.MIN_PODER
        elif nuevo_poder > parametros.MAX_PODER:
            self._poder = parametros.MAX_PODER
        else:
            self._poder = nuevo_poder

    @property
    def defensa(self) -> int:
        return self._defensa

    @defensa.setter
    def defensa(self, nueva_defensa):
        if nueva_defensa < parametros.MIN_DEFENSA:
            self._defensa = parametros.MIN_DEFENSA
        elif nueva_defensa > parametros.MAX_DEFENSA:
            self._defensa = parametros.MAX_DEFENSA
        else:
            self._defensa = nueva_defensa

    @property
    def agilidad(self) -> int:
        return self._agilidad

    @agilidad.setter
    def agilidad(self, nueva_agilidad):
        if nueva_agilidad < parametros.MIN_AGILIDAD:
            self._agilidad = parametros.MIN_AGILIDAD
        elif nueva_agilidad > parametros.MAX_AGILIDAD:
            self._agilidad = parametros.MAX_AGILIDAD
        else:
            self._agilidad = nueva_agilidad

    @property
    def resistencia(self) -> int:
        return self._resistencia

    @resistencia.setter
    def resistencia(self, nueva_resistencia):
        if nueva_resistencia < parametros.MIN_RESISTENCIA:
            self._resistencia = parametros.MIN_RESISTENCIA
        elif nueva_resistencia > parametros.MAX_RESISTENCIA:
            self._resistencia = parametros.MAX_RESISTENCIA
        else:
            self._resistencia = nueva_resistencia

    def ataque(self) -> int:
        # Dado que es igual para todos lo combatientes, 
        # no es necesario que sea abstracta, pero se hereda igual
        ataque = round((self.poder + self.agilidad + self.resistencia) *
                       ((2 * self.vida) / self.vida_maxima))
        return ataque

    def curarse(self, cantidad):
        # Dado que es igual para todos lo combatientes, 
        # no es necesario que sea abstracta, pero se hereda igual
        self.vida += cantidad # se mantiene en los limites por el property
    
    @abstractmethod
    def atacar(self, rival):
        pass

    @abstractmethod
    def evolucionar(self, item):
        pass

    @abstractmethod
    def __str__(self):
        pass


class Guerrero(Combatiente):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.precio = parametros.PRECIO_GUE
        self.tipo = "Guerrero"

    def atacar(self, rival) -> None:
        daño = max(1, round(self.ataque() - rival.defensa))
        rival.vida -= daño
        self.agilidad = self.agilidad * (1 - parametros.CANSANCIO / 100)

    def evolucionar(self, item) -> Combatiente:
        if item.tipo == "Pergamino":
            evolucion = MagoDeBatalla(self.nombre, self.vida_maxima, self.poder,
                                      self.defensa, self.agilidad, self.resistencia)
        elif item.tipo == "Armadura":
            evolucion = Paladín(self.nombre, self.vida_maxima, self.poder,
                                self.defensa, self.agilidad, self.resistencia)
        elif item.tipo == "Lanza": # No deberia pasar nunca por estructura del codigo
            print("No se puede evolucionar a un Guerrero con una lanza")
            return None
        return evolucion

    def __str__(self) -> str:
        return f"¡Hola! Soy {self.nombre}, un Guerrero con {self.vida} / {self.vida_maxima}" + \
            f" de vida, {self.ataque()} de ataque, {self.defensa} de defensa."


class Caballero(Combatiente):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.precio = parametros.PRECIO_CAB
        self.tipo = "Caballero"

    def atacar(self, rival) -> None:
        numero = random.randint(1, 100)
        if numero < parametros.PROB_CAB:
            rival.poder = rival.poder * (1 - parametros.RED_CAB / 100)
            daño = max(1, round((self.ataque() * (parametros.ATQ_CAB / 100)) - rival.defensa))
            rival.vida -= daño
        else:
            daño = max(1, round(self.ataque() - rival.defensa))
            rival.vida -= daño
        self.resistencia = self.resistencia * (1 - parametros.CANSANCIO / 100)

    def evolucionar(self, item) -> Combatiente:
        if item.tipo == "Pergamino":
            evolucion = CaballeroAcano(self.nombre, self.vida_maxima, self.poder,
                                       self.defensa, self.agilidad, self.resistencia)
        elif item.tipo == "Armadura": # No deberia pasar nunca por estructura del codigo
            print("No se puede evolucionar a un Caballero con una armadura")
            return None
        elif item.tipo == "Lanza":
            evolucion = Paladín(self.nombre, self.vida_maxima, self.poder,
                                self.defensa, self.agilidad, self.resistencia)
        return evolucion

    def __str__(self) -> str:
        return f"¡Hola! Soy {self.nombre}, un Caballero con {self.vida} / {self.vida_maxima}" + \
            f" de vida, {self.ataque()} de ataque, {self.defensa} de defensa."


class Mago(Combatiente):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.precio = parametros.PRECIO_MAG
        self.tipo = "Mago"

    def atacar(self, rival) -> None:
        numero = random.randint(1, 100)
        if numero < parametros.PROB_MAG:
            defensa_alterada = rival.defensa * (1 - parametros.RED_MAG / 100)
            daño = max(1, round((self.ataque() * (parametros.ATQ_MAG / 100)) -
                                (defensa_alterada * ((100 - parametros.RED_MAG) / 100))))
            rival.vida -= daño
        else:
            daño = max(1, round(self.ataque() - rival.defensa))
            rival.vida -= daño
        self.resistencia = self.resistencia * (1 - parametros.CANSANCIO / 100)
        self.agilidad = self.agilidad * (1 - parametros.CANSANCIO / 100)

    def evolucionar(self, item) -> Combatiente:
        if item.tipo == "Pergamino": # No deberia pasar nunca por estructura del codigo
            print("No se puede evolucionar a un Mago con un Pergamino")
            return None
        elif item.tipo == "Armadura":
            evolucion = CaballeroArcano(self.nombre, self.vida_maxima, self.poder,
                                        self.defensa, self.agilidad, self.resistencia)
        elif item.tipo == "Lanza":
            evolucion = MagoDeBatalla(self.nombre, self.vida_maxima, self.poder,
                                      self.defensa, self.agilidad, self.resistencia)
        return evolucion

    def __str__(self) -> str:
        return f"¡Hola! Soy {self.nombre}, un Mago con {self.vida} / {self.vida_maxima}" + \
            f" de vida, {self.ataque()} de ataque, {self.defensa} de defensa."


class Paladín(Guerrero, Caballero):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.tipo = "Paladín"

    def atacar(self, rival) -> None:
        numero = random.randint(1, 100)
        if numero < parametros.PROB_PAL:
            super(Caballero, self).atacar(rival)
        else:
            super(Guerrero, self).atacar(rival)
        self.resistencia = self.resistencia * (1 + parametros.AUM_PAL / 100)

    def evolucionar(self, item) -> None: # No deberia pasar nunca por estructura del codigo
        print("No se puede evolucionar a un Paladin con ningun item")
        return None

    def __str__(self) -> str:
        return f"¡Hola! Soy {self.nombre}, un Paladín con {self.vida} / {self.vida_maxima}" + \
            f" de vida, {self.ataque()} de ataque, {self.defensa} de defensa."


class MagoDeBatalla(Guerrero, Mago):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.tipo = "Mago de Batalla"

    def atacar(self, rival) -> None:
        numero = random.randint(1, 100)
        if numero < parametros.PROB_MDB:
            super(Mago, self).atacar(rival)
        else:
            super(Guerrero, self).atacar(rival)
        self.defensa = self.defensa * (1 + parametros.DEF_MDB / 100)
        self.agilidad = self.agilidad * (1 - parametros.CANSANCIO / 100)

    def evolucionar(self, item) -> None: # No deberia pasar nunca por estructura del codigo
        print("No se puede evolucionar a un Mago de Batalla con ningun item")
        return None

    def __str__(self) -> str:
        return f"¡Hola! Soy {self.nombre}, un Mago de Batalla con {self.vida} /" + \
            f"{self.vida_maxima} de vida, {self.ataque()} de ataque, {self.defensa} de defensa."


class CaballeroArcano(Caballero, Mago):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.tipo = "Caballero Arcano"

    def atacar(self, rival) -> None:
        numero = random.randint(1, 100)
        if numero < parametros.PROB_CAR:
            super(Caballero, self).atacar(rival)
        else:
            super(Mago, self).atacar(rival)
        self.agilidad = self.agilidad * (1 + parametros.AUM_CAR / 100)
        self.poder = self.poder * (1 + parametros.AUM_CAR / 100)
        self.resistencia = self.resistencia * (1 - parametros.CANSANCIO / 100)

    def evolucionar(self, item) -> None: # No deberia pasar nunca por estructura del codigo
        print("No se puede evolucionar a un Caballero Arcano con ningun item")
        return None

    def __str__(self) -> str:
        return f"¡Hola! Soy {self.nombre}, un Caballero Arcano con {self.vida} /" + \
            f"{self.vida_maxima} de vida, {self.ataque()} de ataque, {self.defensa} de defensa."
