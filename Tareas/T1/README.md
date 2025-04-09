# Tarea 1: DCCiudad 🚈🐈

## Consideraciones generales

- La tarea se realizo completamente.

- En cuanto a la Parte 1, **realizaron todas las funciones** y todas cumplieron con todos los test dispuestos.

- Por otro lado, en la Parte 2 se realizó todo lo pedido, pudiendo verificar el nombre de la red y la estacion, ser aprueba de todo tipo de errores (bajo las asunciones hechas), indicar el nombre de la red y la estacion indicada e igualmente incorporar las opciones funcionales: mostrar red, encontrar ciclo más corto, asegurar ruta y salir del programa.

- Archivo **ejemplo.py** no fue modificado.

### Cosas implementadas y no implementadas:
- ❌  **NO** completé lo pedido
- ✅ si completé **correctamente** lo pedido
- 🟠 si el item está **incompleto** o tiene algunos errores

- **Parte 1** -  *Funcionalidades*: ✅
    1. **informacion_red**: ✅
    2. **agregar_tunel**: ✅
    3. **tapar_tunel**: ✅
    4. **invertir_tunel**: ✅
    5. **nivel_conexiones**: ✅
    6. **rutas_posibles**: ✅
    7. **ciclo_mas_corto**: ✅
    8. **estaciones_intermedias**: ✅
    9. **estaciones_intermedias_avanzado**: ✅
    10. **cambiar_planos**: ✅
    11. **asegurar_ruta**: ✅

- **Parte 2** -  *Menu*: ✅
    1. **Menu es a prueba de todo tipo de errores**: ✅
    2. **Menu indica el nombre de la red y la estacion indicada**: ✅
    3. **4 opciones** funcionales con su respectivo llamado a funcion: ✅
    4. Opción **Salir** permite salir del programa: ✅
    5. Luego de ejecutar una opción distinta a Salir, se **vuelve al menu**: ✅

- ***Aspectos Generales***: ✅
1. Modularización: ✅
2. PEP8: ✅

## Ejecución
 ```main.py``` en ```\njllanos-iic2233-2024-1\Tareas\T1```

## Librerías
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```os```: ```path.exists(), path.join() / red.py | main.py```
2. ```sys```: ```argv, exit() / main.py```
3.  ```copy```: ```deepcopy / red.py```

## Supuestos y consideraciones adicionales
Los supuestos que realicé durante la tarea son los siguientes:

1. Todos las indicados en el Enunciado:
    1) Para todos los metodos de RedMetro se asumio que el nombre de esta estación existe en la red.
    2) En invertir_tunel() dentro de la clase RedMetro se asume que estacion_1 y estacion_2 siempre serán distintas.
    3) Para los argumentos de la linea de comandos se asume que siempre será una palabra por agumento en el orden indicado dentro del enunciado.
    4) **Dentro del menu, en asegurar ruta**, se asume que el usuario ingresara correctamente los datos (nombre de estacion existente y numero entero).
2. Los archivos que contienen la informacion del metro son de extension ".txt" y estan en el formato ocupado en los otorgados. Junto con ello, en caso de agregarse extras, deben estar en la carpeta "data" para asi no afectar a los paths ocupados. Esto ya que en el enunciado se da a entender estas suposiciones por los ejemplos utilizados y lo dicho, aunque, sin embargo, no se menciona de forma explicita.

## Referencias de código externo

Para realizar mi tarea saqué código de:
1. https://www.geeksforgeeks.org/how-to-use-sys-argv-in-python: este hace posible guardar en variables lo escrito en la linea de comandos y aplicar funciones sobre "sys.argv" y está implementado en el archivo main.py en las líneas 1, 6, 11 y 12 y exporta una libreria externa (sys) la cual cuenta con la función "argv" para así trabajar con lo escrito en las lineas de comando.
2. https://micro.recursospython.com/recursos/como-terminar-un-programa.html#:~:text=V%C3%ADa%20la%20funci%C3%B3n%20est%C3%A1ndar%20sys,exit()%20: este hace posible terminar un programa y está implementado en el archivo main.py en las líneas 9, 18, 36 y 76 y mediante libreria externa (sys) la cual cuenta con la función "exit" perimte cerrar el programa iniciado con el usuario en la linea de comandos.
3. https://www.codigopiton.com/como-hacer-un-menu-de-usuario-en-python/: este ayudó como inspiración y base para la estructura y funcionamieto del menu y la creacion de un diccionario de utilidad y está implementado en el archivo main.py desde la línea 42 a la 101 y mediante la definicion de distintas funciones permite que el menu funcione e imprima de manera correcta en una especie de loop generado en generar_menu() (No es textual en su mayoria, pero si en algunos elementos y estructura).
4. https://rico-schmidt.name/pymotw-3/copy/index.html: este hace posible copiar meramente el contenido de un elementos de un objeto y está implementado en el archivo red.py en las líneas 3 y 148 y exporta una libreria externa (copy) la cual cuenta con la función "deepcopy" copiar el contenido de un elemento de un objeto para poder modificarlo sin afectar al objeto ni su elemento original.