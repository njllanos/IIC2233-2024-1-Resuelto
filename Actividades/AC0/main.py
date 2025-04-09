from entities import Item, Usuario
from utils.pretty_print import print_usuario, print_canasta, print_items
import os

def cargar_items():
    items = []
    ruta = os.path.join("utils", "items.dcc")
    with open(ruta, 'r') as file:
        for linea in file:
            linea = linea.strip()
            linea = linea.split(",")
            item = Item(linea[0], int(linea[1]), int(linea[2]))
            items.append(item)
    return items

def crear_usuario(tiene_suscripcion: bool):
    usuario = Usuario(tiene_suscripcion)
    print_usuario(usuario)
    return usuario

if __name__ == "__main__":
    usuario = crear_usuario(tiene_suscripcion = True)
    items = cargar_items()
    print_items(items)
    for item in items:
        usuario.agregar_item(item)
    print_canasta(usuario)
    usuario.comprar()
    print_usuario(usuario)