import sys
import os
import json
from PyQt6.QtWidgets import QApplication
from frontend.ventana_inicio import VentanaInicio
from backend.logica_inicio import VentanaInicioBackend
from frontend.ventana_juego import VentanaJuego
from backend.logica_juego import VentanaJuegoBackend
from backend.cliente import Cliente

if __name__ == '__main__':
    def hook(type, value, traceback) -> None:
        print(type)
        print(traceback)
    
    sys.__excepthook__ = hook

    with open(os.path.join("cliente", "parametros.json"), "rb") as archivo_json:
        parametros = json.load(archivo_json)
    port = 3247 if len(sys.argv) < 2 else int(sys.argv[1])
    host = parametros["host"]

    app = QApplication([])

    cliente = Cliente(port, host)

    if cliente.conectado == True:

        # Entidades
        ventana_inicio = VentanaInicio()
        logica_inicio = VentanaInicioBackend()
        ventana_juego = VentanaJuego()
        logica_juego = VentanaJuegoBackend()

        # Señales inicio
        ventana_inicio.senal_ordenar_puntajes.connect(logica_inicio.ordenar_puntajes)
        logica_inicio.senal_mensaje_error.connect(ventana_inicio.mensaje_error)
        logica_inicio.senal_empezar_partida.connect(ventana_inicio.comenzar)
        ventana_inicio.senal_verificar_nombre.connect(logica_inicio.verificar_nombre_usuario)
        ventana_inicio.senal_jugar_partida.connect(logica_juego.comenzar)

        # Senales Juego
        logica_juego.senal_adaptar_puzzle.connect(ventana_juego.adaptar_puzzle)
        ventana_juego.senal_posicion_inicial_pepa.connect(logica_juego.posicion_inicial_pepa)
        logica_juego.senal_mostrar_pepa.connect(ventana_juego.aparecer_pepa)
        ventana_juego.senal_volver_inicio.connect(ventana_inicio.mostrar_ventana)
        ventana_juego.senal_tecla.connect(logica_juego.revisar_colisiones_pepa)
        ventana_juego.senal_interacion_g.connect(logica_juego.interaccion_g)
        logica_juego.senal_aparecer_lechuga.connect(ventana_juego.agregar_lechuga)
        logica_juego.senal_aparecer_poop.connect(ventana_juego.aparecer_poop)
        logica_juego.senal_desaparecer_lechuga.connect(ventana_juego.quitar_lechuga)
        logica_juego.pepa.senal_actualizar_pixmap.connect(ventana_juego.lista_pixmap)
        logica_juego.pepa.senal_mover_label.connect(ventana_juego.timer_mover_pepa.start)
        logica_juego.pepa.senal_actualizar_label.connect(ventana_juego.actualizar_label_pepa)
        logica_juego.pepa.senal_mover_label.connect(ventana_juego.timer_animacion_pepa.start)
        logica_juego.senal_mostrar_sandia.connect(ventana_juego.aparecer_sandia)#
        logica_juego.senal_desaparecer_sandia.connect(ventana_juego.desaparecer_sandia)
        ventana_juego.senal_sandia_clickeada.connect(logica_juego.sandia_clickeada)
        logica_juego.senal_actualizar_tiempo.connect(ventana_juego.actualizar_tiempo)
        ventana_juego.senal_pausa.connect(logica_juego.pausar_juego)
        ventana_juego.senal_reanudar.connect(logica_juego.reanudar)
        logica_juego.senal_perder_pop.connect(ventana_juego.mensaje_perder)
        ventana_juego.senal_musica_fondo.connect(logica_juego.administar_musica_fondo)
        ventana_juego.senal_cheatcode_inf.connect(logica_juego.cheatcode_inf)
        ventana_juego.senal_cheatcode_mute.connect(logica_juego.cheatcode_mute)
        ventana_juego.senal_comprobar_puzzle.connect(logica_juego.enviar_solucion)
        logica_juego.senal_ganar_pop.connect(ventana_juego.mensaje_ganar)
        logica_juego.senal_solucion_erronea.connect(ventana_juego.mensaje_solucion_erronea)
        logica_juego.senal_mensaje_desconexion_pop.connect(ventana_inicio.mensaje_desconexion)
        logica_juego.senal_cerrar_ventana.connect(ventana_juego.salir)

        # Cliente
        logica_juego.senal_enviar_solucion.connect(cliente.enviar_solucion)
        cliente.senal_mensaje_servidor.connect(logica_juego.mensaje_servidor)
        cliente.senal_error_serivor.connect(logica_juego.error_servidor)

        sys.exit(app.exec())
    else:
        print("No se ha podido conectar al servidor")