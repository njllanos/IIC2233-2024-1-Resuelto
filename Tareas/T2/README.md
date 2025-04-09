# Tarea 2: DCCombatientes 🐈⚔️

## Consideraciones generales:

- La tarea se **realizó completamente**, incuyendo todos sus puntos.

- Se dividió lo hecho en **distintos archivos con nombres explicativos** de lo que contienen, los cuales se utilizan para la ejecución de main.py.

-  En cuanto al funcionamiento del programa, este puede ser **ejecutado por normalidad**, el cual es **a prueba de errores**. La dificultad y **nivelación del juego son arbitrarios y dependen de los parametros** contenidos en el archivo "parametros.py".

### Cosas implementadas y no implementadas:

#### Programación Orientada a Objetos: 12 pts (10%)
##### ✅ Definición de clases, herencia y *properties*

- Se utilizaron todos los conceptos claves pedidos dentro del código (herencia, clases abstractas, polimorfismo y properties) para la creación de clases. Estos se pueden apreciar en el archivo combatientes.py, en donde fueron usados correctamente cuando fue conveniente y pertinente hacerlo. Además de este archivo, en los otros archivos de clases, items.py y ejercito.py se pueden evidenciar algunos de estos conceptos también. Más detalle de esto en donde se explica "Combatientes".

#### Preparación del programa: 10 pts (8%)
##### ✅ Inicio de la partida

- Se inicia el programa al ejecutar el programa según sus indicaciones explicitadas, en donde, en caso de no haber errores de formato de los archivos o de forma ejecución, se comienza con el menú de inicio, el cual se copió el formato del mostrado en el enunciado.

#### Entidades: 56 pts (47%)
##### ✅ Ejército
- Clase que contiene atributos como; sus combatientes (almacenados en una lista), oro (el cual tiene su respectiva property) y ronda (el cual indica la ronda en la que está el usuario actualmente). Además, contiene métodos para presentarse y combatir (contra otro ejército) según lo especificado en el enunciado.
##### ✅ Combatientes:
- Se creó una clase padre (Combatientes), la cual contiene diversos atributos con propertys para la limitación de sus valores en caso de ser necesarias y métodos abstractos para la implementación de las clases hijas. Luego se desarrollaron los 3 combatientes básicos que heredaron de la clase "Combatiente" con sus respectivos métodos personalizados. Finalmente, para los combatientes evolucionados (que combinan 2 básicos), se usó multiherencia de los combatientes básicos que combinan para luego definir sus métodos según el enunciado.
##### ✅ Ítems
- Se creó una clase padre de ítem y luego se heredó está para hacer los ítems específicos del enunciado. Cada una de estas últimas tiene un método "identificar_aplicables", la cual sirve para identificar cuáles combatientes de un ejército se le puede aplicar el ítem.

#### Flujo del programa: 30 pts (25%)
##### ✅ Menú de Inicio
- Se imitó el mostrado en el enunciado, el cual funciona correctamente y es aprueba de errores.
##### ✅ Menú Tienda
- Se imitó el mostrado en el enunciado, el cual funciona correctamente y es aprueba de errores. En caso de que el dinero sea menor al de la compra, se muestra un error en la compra y su razón y se vuelve al menú de tienda.
##### ✅ Selección de gato
- Se imitó el mostrado en el enunciado, el cual funciona correctamente y es aprueba de errores. En caso de que ningún gato se pueda mostrar en el menú, se muestra un mensaje de error antes de mostrar el menú de gato y se vuelve al menú de tienda.
##### ✅ Fin del Juego
-  Se imprime un mensaje antes de finalizar el juego (se comletaron las 3 rondas), ya sea porque se ha ganado o porque se decidió cerrar el programa desde el menú de inicio.
##### ✅ Robustez
- Programa es aprueba de todos los errores que se dicen que se tienen que resguardar en el enunciado y más.

#### Archivos: 12 pts (10%)
##### ✅ Archivos .txt
- Se leen con las funciones hechas en funciones.py, los cuales las leen y ven si hay errores de formato.
##### ✅ parametros.py
- Se utilizó el mismo formato que el utilizado en el enunciado y se definieron y usaron todos los nombrados en el enunciado e incluso algunos más.

#### Otros
##### ✅ Modularización
##### ✅ PEP8


## Ejecución:
El módulo principal de la tarea a ejecutar es  ```main.py``` en ```\njllanos-iic2233-2024-1\Tareas\T2```. Además se debe crear los siguientes archivos y directorios adicionales:
1. ```facil.txt``` en ```\T2\data```
2. ```intermedio.txt``` en ```\T2\data```
3. ```dificl.txt``` en ```\T2\data```


## Librerías:
La lista de librerías externas utilizadas son las siguientes:

1. ```os```: ```path.exists(), path.join() / funciones.py```
2. ```sys```: ```.argv, .exit() / main.py | funciones.py```
3.  ```random```: ```.randint, .choice / combatientes.py | funciones.py```
3.  ```abc```: ```ABC, abstractmethod / combatientes.py | items.py```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```combatientes```: Contiene a ```Guerrero```, ```Caballero```, ```Mago``` y todos los (otros) tipos de combatientes con sus respectivos metodos y atributos, además de la clase padre de los combatientes.
2. ```ejercito```: Contiene a ```Ejercito``` con sus respectivos metodos y atributos.
3. ```items```: Contiene a ```Lanza```, ```Pergamino```, ```Armadura``` y la clase padre de items con sus respectivos metodos y atributos.
4. ```parametros```: Contiene a los parametros del código.
4. ```funciones```: Contiene las funciones necesarias para el funcionamiento del programa, siendo este dividio en dos partes; para la lectura de los archios y para el funcionamiento del menú.

## Supuestos y consideraciones adicionales:
Los supuestos que realicé durante la tarea son los siguientes:

1. Para combatir, al no poder usar threads, se considero que **ataca primero el usuario y luego el rival (ocurriendo siempre las 2, incluso si luego del ataque queda sin vida)**, para luego verificar si siguen en pie.

2. Se supuso que **luego de ganar (terminar las 3 rondas) se termina el programa**, ya que no se especifica que hacer y no existen más rondas por realizar ni combatientes que enfrentar en la dificultad seleccionada.

3. Se supuso que **al haber notificado los posibles errores de formato en alguno de los archivos se termina el programa**, dado que no tendría sentido correr el programa con un error.

4. Se supuso que **si no se tienen combatientes en el ejercito** y se ejecuta las opción 2 del menu principal ("Ejercito") para mostrar el ejercito, **se imprime un mensaje diferenciado**, dado que no tendría sentido conservar el mismo formato si no hay ningun combatiente en el ejercito.

5. En los enfrentamientos, **cuando se termina la ronda, en caso de que empaten** (ambos ejercitos terminen sin combatientes), se toma como que el **usuario pierde el juego**, ya que según se interpreta del enunciado que eso no es "completar la ronda".

6. Del enunciado se da a entender y se hace la supocición de que, ya sea **en el archivo de unidades o cualquiera correspondiente a los ejercitos de dificultades, si uno de los valores asociado al orden explicitado en el enunciado esta fuera de su rango especifico del atributo, se considera que el formato del archivo esta malo** y se imprime el error.

## Referencias de código externo:

Para realizar mi tarea saqué código de:
1. \<[https://help.uis.cam.ac.uk/system/files/documents/formatting.pdf]()>: este lo utilicé implicitamente para entender e implementar el relleno espacios determinados entre strings y está implementado en el archivo <funciones.py> en la línea <207> y hace que se rellenen con espacios hasta cierto caracter esplecitado al imprimir el string.
2. \<[https://github.com/AntonioEscobar01/IIC2233-2023-1-Resuelto/tree/main/Tareas/T1]()>: este lo utilicé implicitamente para inspirarme en la estructura de mi código (como la manera de dividir los archivos creados, el formato de parametros.py y cosas similares no de código en sí), no obstante no se implementó nada textual, por lo que no está implementado en ningun archivo ni linea en específico. De esta manera, lo que hace es que sea una carpeta y código más ordenado y con un formato más correcto.