
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
        #random point in the image
        point = Point(random.uniform(0, 500), random.uniform(0, 500))
        #pixel color
        pixel = 0

        for source in sources:

            #calculates direction to light source
            
            dir = source-point

            #add jitter
            #dir.x += random.uniform(0, 25)
            #dir.y += random.uniform(0, 25)

            #distance between point and light source
            length = ray.length(dir)

            color = PathTraycing (dir, point, 0, source)

            if color != 0:

                intensity = (1-(length/500))**2
                #print(len)
                #intensity = max(0, min(intensity, 255))
                values = (ref[int(point.y)][int(point.x)])[:3]
                #combine color, light source and light color
                values = values * intensity * light
                
                #add all light sources 
                pixel += values
            

            #average pixel value and assign
            px[int(point.x)][int(point.y)] = pixel // len(sources)




 #Queremos saber si hay una forma que el punto x sea intersecado por la luz. Ya sea directamente o por rebote.

maxRebotes = 1

def PathTraycing (dir, point, rebote, source):

    if rebote >= maxRebotes:

        #print("Rebotó demasiado")
        return 0 

    reboundPoint = Point(501,501)
    free  = True

    for seg in segments: # La idea es en vez de revisar todos los segmentos escoger el más cercano

        length = ray.length(dir)

        dist = ray.raySegmentIntersect(point, dir, seg[0],seg[1]) #Compruebo si hay intersección 

        if dist[0] !=-1 and dist[0] < length: #Hay rebote

            #print("Rebotó en" + str(dist[1].__str__() ) )

            dir = source - dist[1]

            free = False

            #Solo cambiarlo si es el punto intersecado es el más cercano al punto de todos los que han habido

            if (  (dist[1].x - point.x) <= reboundPoint.x and (dist[1].y - point.y) <= reboundPoint.y):

                reboundPoint = dist[1]

        #else: #No hay rebote

            

            #print("Luz directa")


    
    if free == False:  

        if (PathTraycing( dir, reboundPoint, rebote + 1, source) == 0):
            return 0

        #else:

            #Sí rebota

        #Se llama de nuevo a la función, pero con el punto origen es en donde rebotó
        #Sin especularidad = Solo un rebote en una sola dirección 
        

    else: #La luz alcanza con éxito al punto aleatorio

        return 1
        #print("Alcanza la luz con éxito desde " + point.__str__() )


        #Aquí irían los cálculos para el color del pixel o se retornaría el valor




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

#light positions

sources = [ Point(459, 459) ]

#light color
light = np.array([1, 1, 0.75])
#light = np.array([1, 1, 1])

#warning, point order affects intersection test!!


#___________________________________GEOMETRY_______________________________________________________


segments = [
                ([Point(355, 370), Point(397, 370)]),
                ([Point(397, 370), Point(397, 412)]),
                ([Point(397, 412), Point(355, 412)]),
                ([Point(355,412), Point(355, 370)]),
            ]
#Primeros cuatro puntos son un cuadrado verde

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

        screen.fill((0, 0, 0))
        
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

