import gamelib
import png

def paint_nuevo(ancho_lienzo, alto_lienzo):
    '''inicializa el estado del programa con una imagen vacía de ancho_lienzo x alto_lienzo pixels'''
    
    paint = []

    with open("lienzo.csv", "w") as lienzo:
        lienzo.write(f"P3\n{ancho_lienzo} {alto_lienzo}\n255\n")
        lienzo.write(("255 255 255 "*ancho_lienzo+"\n")*alto_lienzo)

    with open("lienzo.csv") as lienzo:
        for _ in range(3):
            lienzo.readline()
        for linea in lienzo:
            linea = linea.rstrip().split()
            fila = []
            for i in range(len(linea)):
                if i % 3 == 0:
                    fila.append(linea[i:i+3])
                    if len(fila) == ancho_lienzo:
                        paint.append(fila)
                        fila = []

    for i in range(len(paint)):
        for j in range(len(paint[i])):
            for k in range(len(paint[i][j])):
                paint[i][j][k] = int(paint[i][j][k])


    return paint


def paint_mostrar(paint, color, ancho_lienzo, alto_lienzo, ancho_interfaz, alto_interfaz, colores_predefinidos, balde):
    '''dibuja la interfaz de la aplicación en la ventana'''

    relacion_ancho = ancho_interfaz/ancho_lienzo**2
    relacion_alto = (alto_interfaz-150)/alto_lienzo**2
    sep_lineas_x = alto_lienzo*relacion_alto
    sep_lineas_y = ancho_lienzo*relacion_ancho
    ancho_rec = ancho_interfaz/ancho_lienzo
    alto_rec = (alto_interfaz-150)/alto_lienzo

    gamelib.draw_begin()

    gamelib.draw_rectangle(0,0,ancho_interfaz,alto_interfaz, fill= "grey")

    for i in range(alto_lienzo):
        gamelib.draw_line(0, (sep_lineas_x)*i, ancho_interfaz, (sep_lineas_x)*i, fill= "black")

    for i in range(ancho_lienzo):
        gamelib.draw_line((sep_lineas_y)*i, (alto_interfaz-150), (sep_lineas_y)*i, 0, fill= "black")

    for i in range(len(colores_predefinidos)):
        colores = list(colores_predefinidos.keys())
        gamelib.draw_rectangle( ancho_interfaz*(i/10)+5, alto_interfaz-100,ancho_interfaz*(i/10)+55, alto_interfaz-50, fill= colores[i])
    
    for j in range(ancho_lienzo):
        for i in range(alto_lienzo):
            gamelib.draw_rectangle(j*(ancho_rec), i*(alto_rec),(j*ancho_rec)+ancho_rec, (i*alto_rec)+alto_rec, fill= decimal_a_hex(paint[i][j]))

    for i in range(3):
        textos = ["Guardar PPM", "Guardar PNG", "Cargar PPM"]
        gamelib.draw_rectangle(ancho_interfaz-150, alto_interfaz-(140-i*50), ancho_interfaz-20, alto_interfaz-(105-i*50))
        gamelib.draw_text(textos[i], ancho_interfaz-85, alto_interfaz-(123-i*50), fill= "black")

    gamelib.draw_rectangle(5, alto_interfaz-40, ancho_interfaz/4, alto_interfaz-5)
    gamelib.draw_text("Ingresar Color",(ancho_interfaz/4+5)/2,(alto_interfaz-(45/2)), fill= "black")
    
    gamelib.draw_rectangle(5, alto_interfaz-145, ancho_interfaz/4, alto_interfaz-110)
    gamelib.draw_text("Reescalar",(ancho_interfaz/4+5)/2,alto_interfaz-(255/2), fill= "black")
    
    gamelib.draw_rectangle(ancho_interfaz/4+5, alto_interfaz-40, ancho_interfaz/4+145, alto_interfaz-5)
    gamelib.draw_text("Atajos", ancho_interfaz/4+75, alto_interfaz-(45/2), fill= "black")
    
    gamelib.draw_rectangle(ancho_interfaz/2-115, alto_interfaz-145,  ancho_interfaz/2+115,alto_interfaz-110)
    gamelib.draw_text(f"Color seleccionado: {color_seleccionado(color, colores_predefinidos)}", ancho_interfaz/2, alto_interfaz-(255/2), fill= "black")

    gamelib.draw_image("deshacer.gif", ancho_interfaz/4+175, alto_interfaz-45)
    gamelib.draw_image("rehacer.gif", ancho_interfaz/4+230, alto_interfaz-45)
    if not balde:
        gamelib.draw_image("balde_false.gif", ancho_interfaz/4+230, alto_interfaz-91)
    else:
        gamelib.draw_image("balde_true.gif", ancho_interfaz/4+230, alto_interfaz-91)


    gamelib.draw_end()


def hex_a_decimal(hex):
    """Convierte de número hexadecimal a número decimal"""

    decimal = []
    try:
        for i in range(len(hex)):
            if i % 2 == 0:
                decimal.append(int(hex[i:i+2], 16))
        return decimal
    except:
        gamelib.say("El valor ingresado no es válido")


def decimal_a_hex(decimal):
    """Convierte de número decimal a número hexadecimal"""
    
    hex = []
    hex_str = ""
    for i in range(len(decimal)):
        if len(hex_str) <= 6:
            hex_str += f"{int(decimal[i]):02x}"
        else:
            hex_str = ""
    hex.append("#"+hex_str)
    return hex


def pintar(paint, color, x, y):
    """Cambia el valor en x, y de paint por el valor del color seleccionado"""
    if paint[y][x] != color:
        paint[y][x] = color


def seleccionar_color(x, y, ancho_interfaz, alto_interfaz):
    """Comprueba si se hizo click sobre una de las posiciones en las que están los cuadrados con los colores por defecto.
        En caso de hacerlo, cambia el color previamente seleccionado por el elegido"""

    colores = ([0,0,0], [255,255,255], [255,0,0], [0,255,0], [0,0,255], [255,255,0])
    for i in range(len(colores)):
        if ancho_interfaz*(i/10)+5 <= x <= ancho_interfaz*(i/10)+55 and alto_interfaz-100 <= y <= alto_interfaz-50:

            return colores[i]


def color_seleccionado(color, colores_predefinidos):
    """Devuelve el color seleccionado. En caso de ser uno por defecto, devuelve su nombre.
        Caso contrario, devuelve su valor hexadecimal como nombre"""

    if str(decimal_a_hex(color)[0]) in colores_predefinidos:
        return colores_predefinidos[str(decimal_a_hex(color)[0])]
    else:
        return decimal_a_hex(color)[0]


def ingresar_color():
    """Permite al usuario ingresar un color de su preferencia con el formato #rrggbb hexadecimal"""

    while True:
        color = gamelib.input("Ingrese el color: ")
        if color and color[0] == "#" and len(color) == 7:
            color = hex_a_decimal(color[1:])
            return color
        elif not color:
            break
        else:
            gamelib.say("El color debe tener el formato #rrggbb")


def guardar_ppm(paint, ancho_lienzo, alto_lienzo):
    """Guarda el archivo actual en formato ppm. En caso de no ingresar ruta específica,
        se guarda en la carpeta de ejecución de main.py"""

    ruta = gamelib.input("Ingrese la ruta del archivo: ")
    if ruta:
        with open(ruta+".ppm","w") as archivo:
            archivo.write(f"P3\n{ancho_lienzo} {alto_lienzo}\n255\n")
            pixeles = ""
            for i in range(len(paint)):
                for j in range(len(paint[i])):
                    for k in range(len(paint[i][j])):
                        pixeles += str(paint[i][j][k])+" "
            archivo.write(pixeles)


def guardar_png(paint):
    """Guarda el archivo actual en formato png con el método de color indexado. En caso de no ingresar ruta específica,
    se guarda en la carpeta de ejecución de main.py"""

    ruta = gamelib.input("Ingrese la ruta del archivo: ")
    paleta = []
    imagen = []
    
    if ruta:
        for i in range(len(paint)):
            for j in range(len(paint[i])):
                if tuple(paint[i][j]) not in paleta:
                    paleta.append(tuple(paint[i][j]))

        for i in range(len(paint)):
            imagen.append([])
            for j in range(len(paint[i])):
                imagen[i].append(paint[i][j])

        for i in range(len(imagen)):
            for j in range(len(imagen[i])):
                imagen[i][j] = paleta.index(tuple(imagen[i][j]))

        ruta = ruta+".png"
        png.escribir(ruta, paleta, imagen)


def cargar_ppm():
    """Permite cargar un archivo de formato ppm"""

    paint = []
    ancho_lienzo = 0
    alto_lienzo = 0
    while True:
        ruta = gamelib.input("Ingrese la ruta del archivo: ")
        if ruta:
            try:
                with open(ruta+".ppm") as archivo:
                    archivo.readline()
                    for linea in archivo:
                        linea = linea.rstrip().split()
                        if len(linea) == 2:
                            ancho_lienzo = int(linea[0])
                            alto_lienzo = int(linea[1])
                        elif len(linea) > 2:
                            fila = []
                            for i in range(len(linea)):
                                if i % 3 == 0:
                                    fila.append(linea[i:i+3])
                                if len(fila) == ancho_lienzo:
                                    paint.append(fila)
                                    fila = []

                for i in range(len(paint)):
                    for j in range(len(paint[i])):
                        for k in range(len(paint[i][j])):
                            paint[i][j][k] = int(paint[i][j][k])

                if ancho_lienzo*alto_lienzo == len(paint[0])*alto_lienzo:
                    return ancho_lienzo, alto_lienzo, paint

            except FileNotFoundError:
                gamelib.say("La ruta ingresada no es válida")
            except:
                gamelib.say("Ha ocurrido un error")
                break
        else:
            break


def reescalar():
    """Reescala el tamaño del lienzo al deseado. Se pierde lo realizado hasta el momento"""

    while True:
        ancho_lienzo = gamelib.input("Ingrese el nuevo ancho: ")
        alto_lienzo = gamelib.input("Ingrese el nuevo alto: ")
        if not ancho_lienzo and not alto_lienzo:
            break
        elif ancho_lienzo.isdigit() and alto_lienzo.isdigit() and int(ancho_lienzo) > 0 and int(alto_lienzo) > 0:
            return int(ancho_lienzo), int(alto_lienzo)
        else:
            gamelib.say("El valor ingresado no es válido")


def chequeo(paint, ancho_lienzo, alto_lienzo):
    """Chequea si el usuario quiere guardar o no lo realizado hasta el momento. 
        En caso de querer, permite guardar lo realizado en formato ppm"""

    while True:
        opcion = gamelib.input("¿Desea guardar lo realizado hasta el momento?\nEn caso de no hacerlo, se borrará\n1 para 'SI'\n2 para 'NO'")
        if opcion == "1":
            guardar_ppm(paint, ancho_lienzo, alto_lienzo)
            return reescalar()
        elif opcion == "2":
            return reescalar()
        elif opcion == None:
            break
        else:
            gamelib.say("La opción ingresada no es válida")


def atajos():
    """Muestra los atajos disponibles"""

    gamelib.say("ATAJOS:\nVer atajos: 'A'\nGuardar PPM: 'Tab'\nGuardar PNG: 'Mayus_block'\nCargar PPM: 'Shift_I'\nIngresar Color: 'Control_I'\nReescalar: 'Alt_I'\nDeshacer = 'Z'\nRehacer = 'Y'\nBalde de pintura = 'B'")


def copia(paint):
    """Realiza una copia de la matriz paint ingresada"""
    
    res = []

    for i in range(len(paint)):
        res.append([])
        for j in range(len(paint[i])):
            res[i].append([])
            for k in range(len(paint[i][j])):
                res[i][j].append(int(paint[i][j][k]))

    return res


def balde(paint, color, x, y, ancho_lienzo, alto_lienzo):
    """Pinta todos los pixeles que se estén "tocando" y sean del mismo color que el primero clickeado de forma recursiva."""

    color_tocado = paint[y][x]
    _balde(paint, color, x, y, color_tocado, ancho_lienzo, alto_lienzo)


def _balde(paint, color, x, y, color_tocado, ancho_lienzo, alto_lienzo):

    if paint[y][x] != color_tocado or paint[y][x] == color:
        return

    for i in range(-1,2):
        for j in range(-1,2):
            if 0 <= y+j < alto_lienzo and 0 <= x+i < ancho_lienzo and paint[y+j][x+i] == color_tocado:
                pintar(paint, color, x, y)
                _balde(paint, color, x+i, y+j, color_tocado, ancho_lienzo, alto_lienzo)