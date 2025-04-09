import parametros


class Ejercito():
    def __init__(self) -> None:
        self.combatientes = [] # lista con los combatientes del ejercito vivos
        self._oro = parametros.ORO_INICIAL
        self.ronda = 1 # ronda en la que se encuentra el juego

    @property
    def oro(self) -> int:
        return self._oro

    @oro.setter
    def oro(self, nuevo_oro):
        if nuevo_oro < parametros.MIN_ORO:
            self._oro = parametros.MIN_ORO
        else:
            self._oro = nuevo_oro

    def __str__(self) -> str:
        if len(self.combatientes) == 0: # si el ejercito esta vacio, no imprimir lo normal
            mensaje_1 = "\nTu ejercito esta vacío, compra gatos en la tienda"
            mensaje_2 = " para añadirlos a tu ejercito."
            return mensaje_1 + mensaje_2
        print("\n*** Este es tu Ejercito Actual ***\n")
        mensaje = ""
        for combatiente in self.combatientes:
            mensaje += str(combatiente) + "\n"
        if len(self.combatientes) > 1:
            mensaje += f"\nTe quedan {len(self.combatientes)} combatientes. ¡Éxito, Guerrero!"
        else: # caso en hay solo un combatiente (se escribe distinto)
            mensaje += f"\nTe queda {len(self.combatientes)} combatiente. ¡Éxito, Guerrero!"
        return mensaje

    def combatir(self, ejercito_rival):
        while (len(self.combatientes) > 0) and (len(ejercito_rival.combatientes) > 0):
            ataque_usuario = self.combatientes[0].atacar(ejercito_rival.combatientes[0])
            ejercito_rival.combatientes[0].atacar(self.combatientes[0])
            # Ambos se atacan, antes de cualquier otra acción
            if self.combatientes[0].vida <= 0:
                self.combatientes.pop(0) # si muere, se saca del ejercito
            if ejercito_rival.combatientes[0].vida <= 0:
                ejercito_rival.combatientes.pop(0)
        if len(self.combatientes) > 0: # si gana el usuario (si "empatan" pierde igual)
            self.oro += parametros.ORO_GANADO
            if self.ronda != 3: # si no era la última ronda
                print("\nGanaste el combate, avanzarás a la siguiente ronda. ¡Mucha suerte!")
            self.ronda += 1
            return self
        else: # si pierde el usuario
            self.combatientes = []
            self.oro = parametros.ORO_INICIAL
            self.ronda = 1
            print("\nPerdiste el combate, volverás a la ronda 1. ¡Intenta otra táctica!")
            return self
