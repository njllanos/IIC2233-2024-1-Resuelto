from abc import ABC, abstractmethod
import parametros


class Item(ABC):
    def __init__(self, *args, **kwargs) -> None:
        pass

    # funcion que identifica si item es cinpatible con combatienes del ejercito
    # como es distinta para cada tipo de item, se define como abstracta
    @abstractmethod
    def identificar_aplicables(self, ejercito):
        pass


class Armadura(Item):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.tipo = "Armadura"
        self.precio = parametros.PRECIO_ARMADURA

    def identificar_aplicables(self, ejercito) -> list:
        # devuelve lista de gatos del ejercito a los cuales el item es aplicable
        gatos_aplicables = []
        for combatiente in ejercito.combatientes:
            if combatiente.tipo in ["Mago", "Guerrero"]:
                gatos_aplicables.append(combatiente)
        return gatos_aplicables


class Pergamino(Item):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.tipo = "Pergamino"
        self.precio = parametros.PRECIO_PERGAMINO

    def identificar_aplicables(self, ejercito) -> list:
        # devuelve lista de gatos del ejercito a los cuales el item es aplicable
        gatos_aplicables = []
        for combatiente in ejercito.combatientes:
            if combatiente.tipo in ["Caballero", "Guerrero"]:
                gatos_aplicables.append(combatiente)
        return gatos_aplicables


class Lanza(Item):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.tipo = "Lanza"
        self.precio = parametros.PRECIO_LANZA

    def identificar_aplicables(self, ejercito) -> list:
        # devuelve lista de gatos del ejercito a los cuales el item es aplicable
        gatos_aplicables = []
        for combatiente in ejercito.combatientes:
            if combatiente.tipo in ["Mago", "Caballero"]:
                gatos_aplicables.append(combatiente)
        return gatos_aplicables
