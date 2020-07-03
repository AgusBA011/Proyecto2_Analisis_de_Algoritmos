
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

        #point = Point(326, 266)

        for source in sources:

            #calculates direction to light source
            


            if ray.distanceBetweenPoints(point, source[0]) <= radioDeIlluminacion:

                #add jitter
                #dir.x += random.uniform(0, 25)
                #dir.y += random.uniform(0, 25)

                dir = source[0] - point

                length = ray.length(dir)

                color = PathTraycing (dir, point, 0, source[0])


                if color[0] != 0:

                    if color[2] > 0: #Luz directa sin rebotes

                        intensity = (1-(length/w))**2

                        values = (ref[int(point.y)][int(point.x)])[:3]

                        values = values * intensity * source[1]


                    else: #Luz con rebota

                        intensity = ((1-(length/w))**2)

                        colorSegmento = (ref[int(color[1].y)][int(color[1].x)])[:3]

                        values = (ref[int(point.y)][int(point.x)])[:3]

                        values = colorSegmento * intensity * source[1]

                        #print(colorSegmento)

                    pixel += values


                #average pixel value and assign
                px[int(point.x)][int(point.y)] = pixel // len(sources)

               # return 0

#Función que se le da un punto de origen y una dirección, y comprueba si esta interseca con algún segmento en pantalla

def checkIntersection(point, dir, source):

    reboundPoint = Point(501,501) #Punto considerado como infinito, se va a reemplazar

    free = True

    segWhereRebound = 0

    length = ray.length(dir)

    length2 = ray.length(ray.normalize(dir))

    for seg in segments: # La idea es en vez de revisar todos los segmentos escoger el más cercano

            typeOfSegment = seg[1]

            segmentPoints = seg[0]

            if (typeOfSegment == "square" ):

                        dist = ray.raySegmentIntersect(point, dir, segmentPoints[0], segmentPoints[1])

                        if dist[0] !=-1 and dist[0] < length2: #Hay rebote

                            #print("Rebotó en" + str(dist[1].__str__() ) )

                            free = False

                            #Solo cambiarlo si es el punto intersecado es el más cercano al punto de todos los que han habido

                            if (  (dist[1].x - point.x) <= reboundPoint.x and (dist[1].y - point.y) <= reboundPoint.y):

                                reboundPoint = dist[1] 

                                segWhereRebound = segmentPoints

            '''
            else: #Es un círculo

                #if (ray.length(segmentPoints[0] - point) <= 350 and ray.length(segmentPoints[1] - point) <= 350 ):

                r = segmentPoints[1]

                center = segmentPoints[0]

                dist = ray.rayCircleIntersection(point, dir, center, r)

                if dist != -1:

                    free = False
                    
                    reboundPoint = Point(0,0)
          
            '''

    if free == False:

        #print(reboundPoint)

        reboundPoint = ray.movePoint(segWhereRebound[0], segWhereRebound[1], dir, reboundPoint)

        return [True, reboundPoint, segWhereRebound] #Choca con un segmento, por ende hay que devolver que sí chocó y en dónde.


    else:

        

        return [False, 0, 0] #En caso opuesto, el rayo no choca.

        


def PathTraycing (dir, point, rebotes, source):  #Queremos saber si hay una forma que el punto x sea intersecado por la luz. Ya sea directamente o por rebote.

    #Hay contacto con la luz

    #print("Direcciones al iniciar<", rebotes)

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

                newDir = ray.newDirection( checkLuz[1], dir, checkLuz[2][0], checkLuz[2][1])

                newRay = PathTraycing ( newDir, checkLuz[1], rebotes + 1, source)

                #print(newDir) #[ 1 o 0, punto, rebotes]


            if limit >= newRaysLimit: #Ninguno de los rayos llegó a la luz

                #print ("Los rayos fallaron")
                return [0] # Pixel negro

            elif (len(newRay) > 1): #Un rayo logró llegar, por ende sí se illumina

                #Hay que mandar cuántos rebotes realizó, el color de que recibirá y el color bleeding

                #print ("Rayo llegó")

                return [1, checkLuz[1], rebotes + 1]


        else: #Con especularidad

            #Hacer el rebote perfecto

            #print("Direccion: ", dir)

            dir.x = -dir.x
            dir.y = -dir.y

            #print("Nueva Direccion: ", dir)

            newRay = PathTraycing ( dir, checkLuz[1], rebotes + 1, source) #Nuevo rayo en una dirección reflejada

            if newRay[0] == 1:

                return [1, checkLuz[1], 1]

    #Segundo rebote
    elif (rebotes == 1):

        checkNewIntersection = checkIntersection(point, dir, source)

        if (checkNewIntersection[0] == True): #En caso de que hay dónde rebotar de nuevo

            print(point, checkNewIntersection[1])

            checkLuz = checkIntersection(checkNewIntersection[1], (source - checkNewIntersection[1] ), source) 

            if checkLuz[0] == False: #Si sirve se retorna

                print("Con el segundo rebote")

                return [1, point, rebotes]

                
    #print("f")
    return [0] #Pixel negro





#_______________________________________________________________________________________________________________________

#Funciones EXTRA
def getFrame():
        
        pixels = np.roll(px,(1,2),(0,1))
        return pixels

#-------------------------------------------------------------------------------

#______________________________PYGAME STUFF_____________________________________

#-------------------------------------------------------------------------------
h,w=500, 500
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


im_file = Image.open("TestColor-Especularidad.png")
ref = np.array(im_file)


#_____________________________________VARIABLES GLOBALES QUE SE PUEDEN CAMBIAR_______________________________________________________

especularidad = True

maxRebotes = 1 #Variable global que define la cantidad de rebotes permitidos por los rayos

newRaysLimit = 10 #Variable que controla la cantidad de nuevos rays que se crean

radioDeIlluminacion = 500


#Posiciones de la luz y colores
light = np.array([1, 1, 0.75])

light2 = np.array([1, 1, 1])

#( Point(250,250), light),          Point(240, 127)

sources = [ (Point(220, 127), light2)] #450



#___________________________________GEOMETRY_______________________________________________________

   

segments =  [
                
                ([Point(385,0), Point(385,500)], "square"), #Pared Azul

                ([Point(186, 189), Point(293, 189) ], "square"), #Cuadrado

                ([Point(293, 189), Point(293, 296) ], "square"),

                ([Point(293, 296), Point(186, 296) ], "square"),

                ([Point(186, 296), Point(186, 189) ], "square"),

               # ([Point(92, 409), 50], "circle")


            ]

 

#________________________________________________________________________________________________




#_____________________________________THREADING__________________________________________________


t = threading.Thread(target = raytrace ) # f being the function that tells how the ball should move
t.setDaemon(True) # Alternatively, you can use "t.daemon = True"
t.start()

#________________________________________________________________________________________________




#Lo agregué yo
fondo= "TestColor-Especularidad.png"
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

        screen.blit(i_lighCircle,(240, 127))


        pygame.display.flip()
        clock.tick(60)


#________________________________________________________________________________________________

