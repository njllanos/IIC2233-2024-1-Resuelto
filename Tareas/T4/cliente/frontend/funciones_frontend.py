from PyQt6 import sip

def borrar_layout(layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    limpiar_layout(item.layout())
            sip.delete(layout)

def limpiar_layout(layout):
        for i in reversed(range(layout.count())): 
                layout.itemAt(i).widget().deleteLater()