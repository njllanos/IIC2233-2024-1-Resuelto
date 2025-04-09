from abc import ABC, abstractmethod
import random


class Vehiculo(ABC):
    identificador = 0
    
    def __init__(self, rendimiento, marca, energia = 120, *args, **kwargs) -> None:
        self.rendimiento = rendimiento
        self.marca = marca
        self.energia = energia
        self.identificador = Vehiculo.identificador
        Vehiculo.identificador += 1
    
    @abstractmethod
    def recorrer(self, kilometros)-> None:
        pass

    @property
    def autonomia(self) -> float:
        return self._energia * self.rendimiento

    @property
    def energia(self) -> int:
        return self._energia
    
    @energia.setter
    def energia(self, valor) -> None:
        if valor < 0:
            self._energia = 0
        else:
            self._energia = valor


class AutoBencina(Vehiculo):
    def __init__(self, bencina_favorita, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bencina_favorita = bencina_favorita

    def recorrer(self, kilometros) -> str:
        if self.autonomia > kilometros:
            litros = int(kilometros/self.rendimiento)
            self._energia -= litros
            return f"Anduve por {kilometros}Km y gaste {litros}L de bencina"
        else:
            km = self.autonomia
            litros = self._energia
            self.energia = 0
            gasto = int(km/self.rendimiento)
            return f"Anduve por {km}Km y gaste {gasto}L de bencina"


class AutoElectrico(Vehiculo):
    def __init__(self, vida_util_bateria, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.vida_util_bateria = vida_util_bateria
    
    def recorrer(self, kilometros) -> str:
        if self.autonomia > kilometros:
            energia = int(kilometros/self.rendimiento)
            self._energia -= energia
            return f"Anduve por {kilometros}Km y gaste {energia}W de energia electrica"
        else:
            km = self.autonomia
            energia = self._energia
            self._energia = 0
            gasto = int(km/self.rendimiento)
            return f"Anduve por {km}Km y gaste {gasto}W de energia electrica"


class Camioneta(AutoBencina):
    def __init__(self, capacidad_maleta, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.capacidad_maleta = capacidad_maleta


class Telsa(AutoElectrico):
    def recorrer(self, kilometros) -> str:
        return super().recorrer(kilometros) + " de forma inteligente"
        

class FaitHibrido(AutoBencina, AutoElectrico):
    def __init__(self,vida_util_bateria = 5, *args, **kwargs) -> None:
        super().__init__(vida_util_bateria = vida_util_bateria, *args, **kwargs)

    def recorrer(self, kilometros) -> str:
        kilometros_electricos = kilometros/2
        kilometros_bencina = kilometros/2
        return AutoBencina.recorrer(self, kilometros_bencina) + " " + AutoElectrico.recorrer(self, kilometros_electricos)
