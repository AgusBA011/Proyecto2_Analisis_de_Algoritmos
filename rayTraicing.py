
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

        point = Point(random.uniform(0, w), random.uniform(0, h))

    
        pixel = 0 #pixel color


        for source in sources:

            #calculates direction to light source
            
            

            dir = source-point

            length = ray.length(dir)


            if ray.distanceBetweenPoints(point, source) <= radioDeIlluminacion:

                #add jitter
                #dir.x += random.uniform(0, 25)
                #dir.y += random.uniform(0, 25)

                color = PathTraycing (dir, point, 0, source)


                if color[0] != 0:

                    if color[2] > 0: #Luz directa sin rebotes

                        intensity = (1-(length/w))**2

                        values = (ref[int(point.y)][int(point.x)])[:3]

                        values = values * intensity * light


                    else: #Luz con rebota

                        intensity = ((1-(length/w))**2)

                        colorSegmento = (ref[int(color[1].y)][int(color[1].x)])[:3]

                        values = (ref[int(point.y)][int(point.x)])[:3]

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

            if (ray.length(seg[0]  - point) <= 350 and ray.length(seg[1]  - point) <= 350 ): #Radio de illuminación


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

        #print(reboundPoint)


    else:

        return [False, 0, 0] #En caso opuesto, el rayo no choca.


def PathTraycing (dir, point, rebotes, source):  #Queremos saber si hay una forma que el punto x sea intersecado por la luz. Ya sea directamente o por rebote.
    '''
    if rebotes >= maxRebotes:

        #print("Rebotó demasiado")

        return [0] # Pixel negro
    '''

    #Hay contacto con la luz

    checkLuz = checkIntersection(point, source - point, source)

    #print(checkLuz[1])

    if (checkLuz[0] == False): #No hay choque con un segmento en dirección a la luz, por lo que por medio de un rebote logró llegar

        #print("Alcanzó la luz")


        return [1, point, rebotes]

    if (rebotes == 0): #Primer rayo

        newRay = [0]

        limit = 0


        if especularidad == False: # SIn especularidad

            while newRay[0] == 0  and limit <= newRaysLimit : #Se crean nuevos rayos

                limit += 1

                newDir = ray.newDirection( point, dir, checkLuz[2][0], checkLuz[2][1])

                newRay = PathTraycing ( newDir, checkLuz[1], rebotes + 1, source)

                #print(limit) #[ 1 o 0, punto, rebotes]


            if limit >= newRaysLimit: #Ninguno de los rayos llegó a la luz

                #print ("Los rayos fallaron")
                return [0] # Pixel negro

            elif (len(newRay) > 1): #Un rayo logró llegar, por ende sí se illumina

                #Hay que mandar cuántos rebotes realizó, el color de que recibirá y el color bleeding

                #print ("Rayo llegó")

                return [1, checkLuz[1], rebotes + 1]


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
h,w=691,691
border=0
pygame.init()
screen = pygame.display.set_mode((h, w))
pygame.display.set_caption("2D Path Tracing")

done = False
clock = pygame.time.Clock()

#init random
random.seed()

#image setup
i = Image.new("RGB", (h, w), (0, 0, 0) )
px = np.array(i)

#reference image for background color


im_file = Image.open("imagen_casa_691x691.jpg")
ref = np.array(im_file)


#_____________________________________VARIABLES GLOBALES QUE SE PUEDEN CAMBIAR_______________________________________________________

especularidad = False

maxRebotes = 2 #Variable global que define la cantidad de rebotes permitidos por los rayos

newRaysLimit = 5 #Variable que controla la cantidad de nuevos rays que se crean


radioDeIlluminacion = 250


#Posiciones de la luz


sources = [ Point(96, 113),  #Cocina

            #Point(97, 268),  #MainRoom

            #Point(626, 39), #Hab1

            #Point(42, 468), #mainRoom

            #Point(236, 526), #HabPeque

            #Point(430, 442) #Hab2

          ] 


#Tienen le siguiente orden: Cocina, Hab1, Mainroom, Mainroom, HabPeque, 


light = np.array([1, 1, 0.75]) #Color de la luz
#light = np.array([1, 1, 1])




#___________________________________GEOMETRY_______________________________________________________


segmentsKitchen = [ 
                    
                    ([Point(51, 10), Point(227, 10)]),
                    ([Point(227, 10), Point(261, 46)]),
                    ([Point(261, 46), Point(264,94)]),
                    ([Point(51, 10), Point(15,46)]),
                    ([Point(15, 46), Point(15,230)]),
                    ([Point(15, 230), Point(36,247)]),
                    ([Point(36, 247), Point(192,247)]),

                    ([Point(236, 237), Point(236,225)]),

                  ]

segmentsHallway = [
                    ([Point(264, 94), Point(459,94)]),
                    ([Point(236, 225), Point(492, 225)]),
                    ([Point(492, 225), Point(513, 202)]),
                    ([Point(513, 202), Point(513, 133)]),

                  ]


segmentsHabitacion1 = [

                        ([Point(459, 94), Point(459,46)]),
                        ([Point(459, 46), Point(495, 9)]),
                        ([Point(495, 9), Point(643, 9)]),
                        ([Point(643, 9), Point(679, 45)]),
                        ([Point(679, 45), Point(679, 202)]),
                        ([Point(679, 202), Point(661, 225)]),
                        ([Point(661, 225), Point(513, 202)]),

                      ]


segmentsHabitacionPeque = [

                            ([Point(292, 482), Point(292, 496)]),

                            ([Point(292, 496), Point(208, 496)]),

                            ([Point(208, 496), Point(208, 660)]),

                            ([Point(208, 660), Point(231, 682)]),

                            ([Point(231, 682), Point(354, 682)]),

                            ([Point(354, 682), Point(374, 660)]),

                            ([Point(374, 660), Point(374, 496)]),

                            ([Point(374, 496), Point(347, 496)]),

                            ([Point(347, 496), Point(347, 454)]),


                          ]

segmentsMainRoom = [

                        ([Point(347, 454), Point(375, 454)]),

                        ([Point(375, 454), Point(375, 394)]),

                        ([Point(36, 247), Point(14,275)]),

                        ([Point(36, 247), Point(14,275)]),

                        ([Point(14, 275), Point(14, 602)]),

                        ([Point(14, 602), Point(36, 624)]),

                        ([Point(14, 602), Point(36, 624)]),

                        ([Point(36, 624), Point(97, 624)]),

                        ([Point(97, 624), Point(97, 676)]),

                        ([Point(97, 676), Point(149, 676)]),

                        ([Point(149, 676), Point(149, 627)]),

                        ([Point(149, 627), Point(176, 627)]),

                        ([Point(176, 627), Point(176, 482)]),

                        ([Point(176, 482), Point(292, 482)]),

                        ([Point(236, 225), Point(236,239)]), 

                        ([Point(236, 225), Point(236,239)]), 

                        ([Point(236, 239), Point(254,239)]),

                        ([Point(254, 239), Point(289,275)]), 

                        ([Point(289, 275), Point(289,323)]),

                        ([Point(289, 323), Point(320, 323)]),

                        ([Point(320, 323), Point(320, 275)])


                    ]


segmentsHap2 = [

                        ([Point(320, 375), Point(357, 240)]),

                        ([Point(357, 240), Point(644, 240)]),

                        ([Point(644, 240), Point(678, 276)]),

                        ([Point(678, 276), Point(678, 516)]),

                        ([Point(678, 516), Point(660, 536)]),

                        ([Point(660, 536), Point(424, 536)]),

                        ([Point(424, 536), Point(404, 516)]),

                        ([Point(404, 516), Point(404, 426)]),

                        ([Point(404, 426), Point(377, 426)])

               ]    

segments = segmentsKitchen + segmentsHallway + segmentsHabitacion1 + segmentsHabitacionPeque + segmentsMainRoom + segmentsHap2

 

#________________________________________________________________________________________________




#_____________________________________THREADING__________________________________________________


t = threading.Thread(target = raytrace ) # f being the function that tells how the ball should move
t.setDaemon(True) # Alternatively, you can use "t.daemon = True"
t.start()

#________________________________________________________________________________________________




#Lo agregué yo
fondo="imagen_casa_691x691.jpg"
img_fondo= pygame.image.load(fondo)

                
img_fondo = pygame.transform.scale(img_fondo,(h,w))
        



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

        #screen.blit(i_lighCircle,(450,450))


        pygame.display.flip()
        clock.tick(30)


#________________________________________________________________________________________________

