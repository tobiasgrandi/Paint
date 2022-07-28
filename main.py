import algopaint
import gamelib
from pila import Pila

ANCHO_INTERFAZ = 600
ALTO_INTERFAZ = 750
COLORES_PREDEFINIDOS = {"#000000": "Negro", 
                        "#ffffff": "Blanco" , 
                        "#ff0000": "Rojo", 
                        "#00ff00": "Verde", 
                        "#0000ff":"Azul", 
                        "#ffff00":"Amarillo"}

def main():
    
    gamelib.title("AlgoPaint")
    gamelib.resize(ANCHO_INTERFAZ, ALTO_INTERFAZ)


    ancho_lienzo = 10
    alto_lienzo = 10
    paint = algopaint.paint_nuevo(ancho_lienzo, alto_lienzo)
    color = [255, 255, 255]
    atajos = ["Control_L", "Alt_L","Shift_L", "Caps_Lock", "Tab", "z", "Z", "y", "Y", "b", "B", "A", "a"]
    balde = None
    pila_paint = Pila()
    pila_rehechos = Pila()


    while gamelib.is_alive():

        algopaint.paint_mostrar(paint, color, ancho_lienzo, alto_lienzo, ANCHO_INTERFAZ, ALTO_INTERFAZ, COLORES_PREDEFINIDOS, balde)

        ev = gamelib.wait()


        if not ev:
            break
        x = ev.x
        y = ev.y
        tecla = ev.key


        if ev.type == gamelib.EventType.ButtonPress and ev.mouse_button == 1 or ev.type == gamelib.EventType.KeyPress:

            if tecla == "??":
                color_prov = algopaint.seleccionar_color(x, y, ANCHO_INTERFAZ, ALTO_INTERFAZ)
                if color_prov:
                    color = color_prov



            if ALTO_INTERFAZ-45 <= y <= ALTO_INTERFAZ-3 and tecla == "??" or tecla in atajos[5:9]:

                if not pila_paint.esta_vacia() and (ANCHO_INTERFAZ/4+175 <= x <=ANCHO_INTERFAZ/4+216 or tecla in atajos[5:7]):
                    pila_rehechos.apilar(paint)
                    paint = pila_paint.desapilar() 

                elif not pila_rehechos.esta_vacia() and (ANCHO_INTERFAZ/4+230 <= x <= ANCHO_INTERFAZ/4+271 or tecla in atajos[7:9]):
                    pila_paint.apilar(paint)
                    paint = pila_rehechos.desapilar()
                    
            elif pila_paint.esta_vacia() or paint != pila_paint.ver_tope():
                pila_paint.apilar(algopaint.copia(paint))



            if (5 <= x <= ANCHO_INTERFAZ/4 and ALTO_INTERFAZ-40 <= y <= ALTO_INTERFAZ-5 and tecla == "??") or tecla == atajos[0]:
                color_prov_2 = algopaint.ingresar_color()
                if color_prov_2:
                    color = color_prov_2


            elif y < (ALTO_INTERFAZ-150) and x < ANCHO_INTERFAZ and tecla == "??":
                x = int(x//(ANCHO_INTERFAZ/ancho_lienzo))
                y = int(y//((ALTO_INTERFAZ-150)/alto_lienzo))
                if balde:
                    algopaint.balde(paint, color, x, y, ancho_lienzo, alto_lienzo)
                else:
                    algopaint.pintar(paint, color, x, y)

                while not pila_rehechos.esta_vacia():
                    pila_rehechos.desapilar()


            elif (5 <= x <= ANCHO_INTERFAZ/4 and ALTO_INTERFAZ-145 <= y <= ALTO_INTERFAZ-110 and tecla == "??") or tecla == atajos[1]:
                
                nuevas_dimensiones = algopaint.chequeo(paint, ancho_lienzo, alto_lienzo)
                if nuevas_dimensiones:
                    ancho_lienzo = nuevas_dimensiones[0]
                    alto_lienzo = nuevas_dimensiones[1]
                    paint = algopaint.paint_nuevo(ancho_lienzo, alto_lienzo)

                    while not pila_paint.esta_vacia():
                        pila_paint.desapilar()
                    while not pila_rehechos.esta_vacia():
                        pila_rehechos.desapilar()


            elif ANCHO_INTERFAZ-150 <= x <= ANCHO_INTERFAZ-20 and tecla == "??" or tecla in atajos[2:5]:

                if ALTO_INTERFAZ-140 <= y <= ALTO_INTERFAZ-105 or tecla == atajos[4]:
                    algopaint.guardar_ppm(paint, ancho_lienzo, alto_lienzo)

                elif ALTO_INTERFAZ-90 <= y <= ALTO_INTERFAZ-55 or tecla == atajos[3]:
                    algopaint.guardar_png(paint)

                elif ALTO_INTERFAZ-40 <= y <= ALTO_INTERFAZ-5 or tecla == atajos[2]:
                    paint_prov = algopaint.cargar_ppm()
                    if paint_prov:
                        ancho_lienzo = paint_prov[0]
                        alto_lienzo = paint_prov[1]
                        paint = paint_prov[2]

                        while not pila_paint.esta_vacia():
                            pila_paint.desapilar()
                        while not pila_rehechos.esta_vacia():
                            pila_rehechos.desapilar()


            elif ANCHO_INTERFAZ/4+5 <= x <= ANCHO_INTERFAZ/4+145 and ALTO_INTERFAZ-40 <= y <= ALTO_INTERFAZ-5 and tecla == "??" or tecla in atajos[11:]:
                algopaint.atajos()


            elif ANCHO_INTERFAZ/4+230 <= x <= ANCHO_INTERFAZ/4+271 and ALTO_INTERFAZ-91 <= y <= ALTO_INTERFAZ-49 and tecla == "??" or tecla in atajos[9:11]:
                if not balde:
                    balde = True
                else:
                    balde = False

gamelib.init(main)