# Tarea 4: DCCome Lechuga 🐢🍉🥬


## Consideraciones generales :octocat:

- La tarea se **realizó completamente**, incuyendo todos sus puntos e integraciones requeridas.

- Se dividieron las implementaciones en **distintos archivos con nombres explicativos** de lo que contienen o su funcionalidad, los cuales se utilizan para la ejecución de main.py para el caso del servidor o del cliente.

- El juego se realizo con ventans de tamaños fijos, los cuales permiten el funcionamiento de de los puzzles entregados a la perfección. Según que puzzles, fuera de los entregados y similares, podría ser necesario ajustar el tamaño de la ventana fijado.

### Cosas implementadas y no implementadas:

#### Entidades: 18.5 pts (21%)
##### ✅ Pepa: Pepa se mueve de forma discreta, pero en la grafica de forma continua. No se sale del tablero y puede cumplir todas las implementaciones pedidas
##### ✅ Sandías: aparecen y pueden ser clickeadas para sumar tiempo. Obs: Al ser ser infinito el tiempo con cheatcode siguen apareciendo pero no tienen efecto en el juego.

#### Interfaz gráfica: 27 pts (30%)
##### ✅ Ventana Inicio: interfaz estetica que cumple con todo lo requerico, salon de la fama, botones, nombre usuario, logo, etc.
##### ✅ Ventana Juego: interfaz estetica que se responde al puzzle seleccionado. Cumple con todos sus botones e informacion.
##### ✅ Fin del *puzzle*: se hace segun las indicaciones del enunciado, apareciendo los pop ups correspondientes y volviendo al menu en caso de que el usuario no haya salido.

#### Interacción: 13 pts (14%)
##### ✅ *Cheatcodes*: Todos los cheatcodes funcionales, teniendo vidas infinitas o muteando los efectos y musica por la pasrtida actual
##### ✅ Sonidos: todos los sonidos funcionales y se escuchan cuando corresponde. Tal como se comenta en consideraciones, los efectos (no considera musica) no se solapan dado que en el enunciado no dice nada al respecto y se considero molestoso para el usuario.

#### *Networking*: 20.5 pts (23%)
##### ✅ Arquitectura: se hace la arquitectura adecuada servidor-cliente con separacion funcional, siendo del tipo pedido.
##### ✅ *Networking*:  cliente y servidor trabajan por separado y servidor tiene la funcion de corregir los puzzles segun las emisiones del cliente conectado.
##### ✅ Codificación y decodifición: se codifica con el metodo pedido.

#### Archivos: 11 pts (12%)
##### ✅ *sprites*: Se mueve Pepa con una animación continua
##### ✅ *puzzle*: pusle aparece de igual manera que se muestra en el enunciado y se puede resolver de forma efectiva.
##### ✅ JSON: se usa json para relación cliente servidor.
##### ✅ parámetros.py: contiene los parametros y rutas utilizadas en el juego dentro de cliente.


## Ejecución:
Para ejecutar la tarea, por parte del servidor este debe ejecutarse en:
1. ```main.py``` en ```servidor\```

Mientras que, en cuanto a los clientes, estos deben ser ejecutados desde:
1. ```main.py``` en ```cliente\```

Además se deben crear los assets en carpetas de nombre ```assets```, tanto en el cliente como en el servidor, estando ambos simplemente en ```cliente\``` y ```servidor\```respectivamente.

Para el caso de ```assets``` del cliente, este debe contener:
1. ```sprites``` en ```cliente\assets\```, esta debe contener todos los elementos .png dispuestos en syllabus con sus mismos nombres, los cuales permiten a la interfaz gráfica mostrar los personajes del juego.
2. ```sonidos``` en ```cliente\assets\```, esta debe contener todos los sonidos utilizados en el juego con los nombres explicitados en el enunciado.
3. ```base_puzzles``` en ```cliente\assets\```, esta debe contener la base de todos los puzzles en el formato explicitado en el enunciado.

Para el caso de ```assets``` del servidor, este debe contener:
1. ```solucion_puzzles``` en ```servidor\assets\```, esta debe contener la solución de todos los puzzles en el formato explicitado en el enunciado, la cual se encuentra en syllabus.


## Librerías:
### Librerías externas utilizadas
Las librerías externas que utilicé estan todas dentro de las permitidas y fueron las siguientes:

1. ```os```
2. ```Pyqt6```
3. ```random```
4. ```sys```
5. ```threading```
6. ```copy```
7. ```json```
8. ```socket```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```funciones_juego.py```: Contiene funciones auxiliares para el funcionamiento del juego y su lógica.
2. ```funciones_cliente.py```: Contiene funciones auxiliares para el funcionamiento del cliente del juego.
3. ```entidades.py```: Contiene la clase ```Pepa``` y ```Sandia```.
4. ```cliente.py```: Contiene la clase ```Cliente```.
5. ```funciones_servidor.py```: Contiene funciones auxiliares para el funcionamiento del servidor del juego.
6. ```servidor.py```: Contiene la clase ```Servidor```.
7. ```parametros.py```: Contiene los parametros para el funcionamiento del juego.
8. ```funciones_frontend.py```: Contiene funciones auxiliares para el funcionamiento de la interfaz del juego.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Los efectos de sonido (no la música de fondo) no se solapan entre sí, osea se reproduce uno y si hay otro efecto durante la duración del anterior este se interrumpe y se reproduce el nuevo. Esto es valido e incluso recomendable, ya que me percate al jugar que el solapamiento de efectos resulta incomodo y poco agradable para el usuario (sobretodo si uno juega rapido).
2. Como consideración, mi teclado tenia un problema al realizar el cheatcode de muteo, por lo que nunca logre hacerlo. Lo probe en otro computador y sí funciono, porbablemente se deba a un error propio del computador y no del código
3. La carpeta ```puntaje.txt``` se encuetra dentro de la carpeta ```cliente```
4. Tal como se explicara en la parte de referencias, basé mi tarea en gran parte a tareas pasadas del curso resueltas previamente subidas resueltas (adaptadas obviamente para este caso), no obstante se realizó un proceso de aprendizaje efectivo en los contenidos evaluados. **La parte de referencias es larga, pero prefiero ser extenso que tener riesgos**.

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. \<https://github.com/AntonioEscobar01/IIC2233-2023-1-Resuelto/tree/main/Tareas/T2>: me base en gran parte de tanto la lógica como la interfaz gráfica del juego de esta fuente. Esto incluye señales, estrucura de código, funciones, entidades, etc. Por ende se podría decir que esta implementado en todos los archivos realizados por mí en la capeta ```cliente``` exepto ```cliente.py``` y ```funciones_cliente.py```. No obstante, gran parte no fue textual sino adaptado. En ```entidades.py``` obtuve de aqui practicamente toda la clase Pepa (linea 8 a 58), incluyendo la función crear_pixmaps, mover_pepa (adaptado) e init y las 3 señales de la linea 9 a 11. En ```funciones_juego.py``` obtuve la funcion segundos_a_string. En ```logica_inicio.py``` obtuve la estructura de codigo y las dos señales de la linea 5 a 6. En ```logica_juego.py``` obtuve la estructura de codigo de la clase realizada, las señales relacionadas a pops, pepa, lechugas, poop, sandias y el tiempo (linea 10 a 23) y también gran parte de las funciones de la clase (al menos en inspiración). Entre estas ultimas, las que fui mas textual, son revisar_colisiones_pepa (linea 76-82), crear_pepa (linea 120-121), disminuir_tiempo (151-159) perder y ganar (202-212), cheatcode_inf (223-227). Recalcar que otras funciones tambien tienen incfluencia y que en mayoria de casos no fue textual sino ideas o logicas. En ```ventana_inicio.py``` obtuve la forma de crear labels, sus fuentes y configuraciones en el init_gui (18-107), incluyendo, con mayor enfasis, la forma de hacer la eleccion de puzzles dentro de la pantalla de inicio (74-77). Ademas tambien obtuve funciones de la clase creada del archivo, como mensaje_error (130-138). En ```ventana_juego.py```, además de la estructura general de la clase, obtuve  las señales relacionadas a pepa, cheatcodes, sandia, pausa y teclas (9-19). Junto con ello, en init e init_gui obtuve la forma de los labels de tiempo, y, especialmente, todo lo relacionado al movimiento de pepa (su label, timers, animaciones, etc.), las teclas, las flag, etc. (21-99). Ademas obtuve ideas y adapte cosas en funciones, como levantar_label (223-224), keyPressEvent (261-291), keyReleaseEvent (293-307), mover_pepa (309-325), actualizar_label (327-329), cambiar_pixmap_pepa (331-337), lista_pixmap (339-400), mousePressEvent (354-359), actualizar_tiempo (365-366), mensajes perder y ganar (371-384). De ```main.py``` tambien se saco inpiración en estrucura y las señales que anteriormente fueron mencionadas.

2. \<https://github.com/AntonioEscobar01/IIC2233-2023-1-Resuelto/tree/main/Tareas/T3>: me base en gran parte de la conexión cliente-servidor y networking de esta fuente. Aqui lo principal que se hizo fue inspirarse en la estructura de lo citado y adaptar y basarse funciones para lograr lo pedido en realción al tema. Similar a lo que ocurre en la referencia anterior, se podría decir que toda la carpeta ```servidor``` y la parte relacionada a networking de la carpeta ```cliente``` (parametros.json, cliente.py y funciones_cliente principalmente) se encuentran basados en la fuente citada. En ```funciones_servidor.py``` se basó en las funciones codificar (14-27) y decodificar (29-40), adaptandolo a los requerimientos del enunciado. En ```main.py``` de servidor se baso en la forma de abrir el servidor (15-19), incluyendo la estructura tambien de ```parametros.json```. En ```servidor.py``` se adaptaron todas las funciones presentes en la clase, incluyendo la estructura de la misma (6-50 y 59-68), siendo en algunas de estas incluso explicitas. En ```cliente```, en ```cliente.py```, al igual que en el servidor se adaptaron todas las funciones presentes en la clase, incluyendo la estructura de la misma, siendo en casi de forma total y explicita (7-48). En ```funciones_cliente.py``` se basó en las funciones codificar y decodificar (3-30), adaptandolo a los requerimientos del enunciado. En ```main.py``` de cliente se baso en la forma de abrir el servidor (18-21), incluyendo la estructura tambien de ```parametros.json```.

3. \<https://doc.qt.io/qt-6/qtimer.html>: obtuve la menera de saber el tiempo restante a un Qtimer y esta implementado en lineas 169, 172, 184 y 188 de ```logica_juego.py```.

4. \<https://doc.qt.io/qt-6/qtimer.html>: obtuve la menera de hacer un loop en musica denrto de la interfaz y esta implementado en la linea 220 de ```logica_juego.py```.

5. \<https://stackoverflow.com/questions/4528347/clear-all-widgets-in-a-layout-in-pyqt>: obtuve la menera de eliminar todo el contenido de un layout y como borrarlo y esta implementado en las lineas 3 a 16 de ```funciones_frontend.py```.

6. \<https://doc.qt.io/qt-6/stylesheet-examples.html>: obtuve la menera de hacer los botones de manera estetica y esta implementado en el frontend en lineas 94-96, 89-91 de ```ventana_inicio.py``` y 49-63 de ```ventana_juego.py```.
7. \<https://doc.qt.io/qt-6/qgridlayout.html>: obtuve la menera de saber la ubicacion de un item dentro de un layout y esta implementado las lineas 192, 179, 159, 158 y 223-224 de ```ventana_juego.py```.
7. \<https://forum.qt.io/topic/97583/solved-how-to-check-if-qmouseevent-pos-inside-a-qwidget>: obtuve la forma de saber si se clickio un label y esta implementado la linea 358 de ```ventana_juego.py```.

## Descuentos
- Se cumple con PEP y no se relaizan malas prácticas.