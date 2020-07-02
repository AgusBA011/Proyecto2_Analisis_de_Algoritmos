
import pygame
import random
import numpy as np 
from PIL import Image

import math
import threading

#Clases and files
from Point import *

import ray

#-------------------------------------------------------------------------------------------------------------------------------
#___________________________________________________PATH RACING__________________________________________________________________

#--------------------------------------------------------------------------------------------------------------------------------


def raytrace():
    #Raytraces the scene progessively

    while True:

        #MONTE CARLO

        point = Point(random.uniform(0, 500), random.uniform(0, 500))

    
        pixel = 0 #pixel color


        for source in sources:

            #calculates direction to light source
            
            dir = source-point

            length = ray.length(dir)

            #add jitter
            #dir.x += random.uniform(0, 25)
            #dir.y += random.uniform(0, 25)

            color = PathTraycing (dir, point, 0, source)


            if color[0] != 0:

                if color[2] > 0: #Luz directa sin rebotes

                    intensity = (1-(length/500))**2

                    values = (ref[int(point.y)][int(point.x)])[:3]

                    values = values * intensity * light


                else: #Luz con rebota

                    intensity = ((1-(length/500))**2)

                    colorSegmento = (ref[int(color[1].y)][int(color[1].x)])[:3]

                    #values = (ref[int(point.y)][int(point.x)])[:3]

                    values = colorSegmento * intensity * light

                    print(colorSegmento)

                pixel += values


            #average pixel value and assign
            px[int(point.x)][int(point.y)] = pixel // len(sources)



#Función que se le da un punto de origen y una dirección, y comprueba si esta interseca con algún segmento en pantalla

def checkIntersection(point, dir, source):

    reboundPoint = Point(501,501) #Punto considerado como infinito, se va a reemplazar

    free = True

    segWhereRebound = 0

    length = ray.length(dir)

    length2 = ray.length(ray.normalize(dir))

    for seg in segments: # La idea es en vez de revisar todos los segmentos escoger el más cercano

            
            dist = ray.raySegmentIntersect(point, dir, seg[0],seg[1]) #Compruebo si hay intersección 

            if dist[0] !=-1 and dist[0] < length2: #Hay rebote

                #print("Rebotó en" + str(dist[1].__str__() ) )

                free = False

                #Solo cambiarlo si es el punto intersecado es el más cercano al punto de todos los que han habido

                if (  (dist[1].x - point.x) <= reboundPoint.x and (dist[1].y - point.y) <= reboundPoint.y):

                    reboundPoint = dist[1] 

                    segWhereRebound = seg


    if free == False:

        return [True, reboundPoint, segWhereRebound] #Choca con un segmento, por ende hay que devolver que sí chocó y en dónde.

    else:

        return [False, 0, 0] #En caso opuesto, el rayo no choca.


def PathTraycing (dir, point, rebotes, source):  #Queremos saber si hay una forma que el punto x sea intersecado por la luz. Ya sea directamente o por rebote.

    if rebotes >= maxRebotes:

        #print("Rebotó demasiado")

        return [0] # Pixel negro


    #Hay contacto con la luz

    checkLuz = checkIntersection(point, source - point, source)

    if (checkLuz[0] == False): #No hay choque con un segmento en dirección a la luz, por lo que por medio de un rebote logró llegar

        #print("Alcanzó la luz")


        return [1, point, rebotes]

    if (rebotes == 0): #Primer rayo

        newRay = [0]

        limit = 0

        if especularidad == False: # SIn especularidad

            while newRay == 0  and limit >= newRaysLimit : #Se crean nuevos rayos

                limit += limit

                newDir = ray.newDirection( point, dir, checkLuz[2][0], checkLuz[2][1])

                newRay = PathTraycing ( checkLuz[1], newDir, rebotes + 1, source)

                #print(newRay)


            if limit >= newRaysLimit: #Ninguno de los rayos llegó a la luz

                                            #print ("Los rayos fallaron")
                return [0] # Pixel negro

            elif (len(newRay) > 1): #Un rayo logró llegar, por ende sí se illumina

                #Hay que mandar cuántos rebotes realizó, el color de que recibirá y el color bleeding

                return [1, checkLuz[1], rebotes]


        else: #Con especularidad

            #Hacer el rebote perfecto

            dir = (-dir.x, -dir.y)

            newRay = PathTraycing ( dir, checkLuz[1], rebotes + 1, source) #Nuevo rayo en una dirección reflejada


    return [0] #Pixel negro


#En caso de que queramos agregar más rebotes hay que hacerlo diferente

#_______________________________________________________________________________________________________________________

#Funciones EXTRA
def getFrame():
        
        pixels = np.roll(px,(1,2),(0,1))
        return pixels

#-------------------------------------------------------------------------------

#______________________________PYGAME STUFF_____________________________________

#-------------------------------------------------------------------------------
h,w=500,500
border=0
pygame.init()
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("2D Path Tracing")

done = False
clock = pygame.time.Clock()

#init random
random.seed()

#image setup
i = Image.new("RGB", (500, 500), (0, 0, 0) )
px = np.array(i)

#reference image for background color


im_file = Image.open("fondo.png")
ref = np.array(im_file)


#_____________________________________VARIABLES GLOBALES QUE SE PUEDEN CAMBIAR_______________________________________________________

especularidad = False

maxRebotes = 2 #Variable global que define la cantidad de rebotes permitidos por los rayos

newRaysLimit = 1 #Variable que controla la cantidad de nuevos rays que se crean


sources = [ Point(459, 459) ] #Posiciones de la luz


light = np.array([1, 1, 0.75]) #Color de la luz
#light = np.array([1, 1, 1])




#___________________________________GEOMETRY_______________________________________________________


segments = [
                ([Point(355, 370), Point(397, 370)]),
                ([Point(397, 370), Point(397, 412)]),
                ([Point(397, 412), Point(355, 412)]),
                ([Point(355,412), Point(355, 370)]),
            ]




#________________________________________________________________________________________________




#_____________________________________THREADING__________________________________________________


t = threading.Thread(target = raytrace ) # f being the function that tells how the ball should move
t.setDaemon(True) # Alternatively, you can use "t.daemon = True"
t.start()

#________________________________________________________________________________________________




#Lo agregué yo
fondo="fondo.png"
img_fondo= pygame.image.load(fondo)

                
img_fondo = pygame.transform.scale(img_fondo,(500,500))
        



lightCircle = "Light Circle.png"
i_lighCircle = pygame.image.load(lightCircle)

i_lighCircle = pygame.transform.scale(i_lighCircle,(20,20))     
        
#Termina lo que agregué



#________________________________________MAIN LOOP__________________________________________________

#main loop
while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

        # Clear screen to black before drawing 

        screen.fill((255, 255, 255))
        
        #screen.blit(img_fondo,(border,border))

        

        '''
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x >= 59 and mouse_x <= 540 and mouse_y >= 61 and mouse_y <= 540:
                
                screen.blit(i_lighCircle,(mouse_x - 10,mouse_y - 10))
        '''

        #print(pygame.mouse.get_pos())

        # Get a numpy array to display from the simulation

        npimage=getFrame()

        # Convert to a surface and splat onto screen offset by border width and height

           
        surface = pygame.surfarray.make_surface(npimage)
        screen.blit(surface, (border, border))

        screen.blit(i_lighCircle,(450,450))


        pygame.display.flip()
        clock.tick(60)


#________________________________________________________________________________________________

