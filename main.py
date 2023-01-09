import pygame
import random
import math
from pygame import mixer

# Inicializar pygame
pygame.init()

# Crear pantalla
pantalla = pygame.display.set_mode((800, 600))

# Título e Icono
pygame.display.set_caption("Invasión Espacial")
icono = pygame.image.load("ovni.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load("Fondo.jpg")

# Agregar música
mixer.music.load('MusicaFondo.mp3')
mixer.music.play(-1)




# Nave
nave = pygame.image.load("cohete.png")
nave_x = 380
nave_y = 500
nave_x_cambio = 0


# Ovni
ovni = []
ovni_x = []
ovni_y = []
ovni_x_cambio = []
ovni_y_cambio = []
cantidad_ovnis = 8

for e in range(cantidad_ovnis):
    ovni.append(pygame.image.load("enemigo.png"))
    ovni_x.append(random.randint(0, 736))
    ovni_y.append(random.randint(50, 100))
    ovni_x_cambio.append(0.1)
    ovni_y_cambio.append(50)



# Bala
bala = pygame.image.load("bala.png")
cantidad_balas = 8
bala_x = 0
bala_y = 500
bala_y_cambio = 0.3
bala_visible = False
bala_fuente = pygame.font.Font('freesansbold.ttf', 20)
bala_text_x = 700
bala_text_y = 10

# Puntuación
puntuacion = 0
fuente = pygame.font.Font('freesansbold.ttf', 32)
texto_x = 10
texto_y = 10


# Texto Game Over
fuente_final = pygame.font.Font('freesansbold.ttf', 100)

def texto_final():
    mi_fuente_final = fuente_final.render("Game Over", True, (255, 255, 255))
    pantalla.blit(mi_fuente_final, (160, 200))


# Texto victoria
fuente_victoria = pygame.font.Font('freesansbold.ttf', 100)

def texto_victoria():
    mi_fuente_victoria = fuente_victoria.render("Ganaste", True, (255, 255, 255))
    pantalla.blit(mi_fuente_victoria, (160, 200))


# Función mostrar puntuacion
def mostrar_puntuacion(x, y):
    texto = fuente.render(f'Puntuación: {puntuacion}', True, (255, 255, 255))
    pantalla.blit(texto, (x, y))

# Función mostrar balas
def mostrar_balas(x, y):
    texto = bala_fuente.render(f'Balas: {cantidad_balas}', True, (255, 255, 255))
    pantalla.blit(texto, (x, y))


# Función jugador
def posicion_nave(x, y):
    pantalla.blit(nave, (x, y))


# Función enemigo
def posicion_ovnis(x, y, ovn):
    pantalla.blit(ovni[ovn], (x, y))


# Función disparar bala
def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(bala, (x + 16, y + 10))



# Función detectar colisiones
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_2 - x_1, 2) + math.pow(y_2 - y_1, 2))
    if distancia < 27:
        return True
    else:
        return False



# Loop del juego
ejecucion = True
while ejecucion:

    # Img de pantalla
    pantalla.blit(fondo, (0, 0))

    # Iterador de Eventos
    for evento in pygame.event.get():

        # Evento cerrar
        if evento.type == pygame.QUIT:
            ejecucion = False

        # Evento presionar teclas
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                nave_x_cambio = -0.1
            if evento.key == pygame.K_RIGHT:
                nave_x_cambio = 0.1
            if evento.key == pygame.K_SPACE:
                cantidad_balas -= 1
                sonido_bala = mixer.Sound('disparo.mp3')
                sonido_bala.play()
                if not bala_visible:
                    bala_x = nave_x
                    disparar_bala(bala_x, bala_y)

        # Evento soltar teclas
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                nave_x_cambio = 0

    # Modificar ubicación nave
    nave_x += nave_x_cambio

    # Mantener dentro de bordes nave
    if nave_x <= 0:
        nave_x = 0
    elif nave_x >= 736:
        nave_x = 736

    # Modificar ubicación ovnis
    for e in range(cantidad_ovnis):

        # Fin del juego
        if ovni_y[e] > 450 or cantidad_balas == -1:
            for k in range(cantidad_ovnis):
                ovni_y[k] = 1200
            texto_final()
            break
        if cantidad_ovnis == 1:
            texto_victoria()
            break



        ovni_x[e] += ovni_x_cambio[e]

    # Mantener dentro de bordes ovnis
        if ovni_x[e] <= 0:
            ovni_x_cambio[e] = 0.1
            ovni_y[e] += ovni_y_cambio[e]
        elif ovni_x[e] >= 736:
            ovni_x_cambio[e] = -0.1
            ovni_y[e] += ovni_y_cambio[e]

        # Colisión
        colision = hay_colision(ovni_x[e], ovni_y[e], bala_x, bala_y)
        if colision:
            cantidad_ovnis -= 1
            sonido_colision = mixer.Sound('Golpe.mp3')
            sonido_colision.play()
            bala_y = 500
            bala_visible = False
            puntuacion += 1
            ovni_x[e] = random.randint(0, 736)
            ovni_y[e] = random.randint(50, 100)

        posicion_ovnis(ovni_x[e], ovni_y[e], e)

    # Movimiento bala
    if bala_y <= -64:
        bala_y = 500
        bala_visible = False

    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio





    posicion_nave(nave_x, nave_y)


    mostrar_puntuacion(texto_x, texto_y)

    mostrar_balas(bala_text_x, bala_text_y)


    # Actualizar
    pygame.display.update()






