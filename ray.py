from Point import *
import random
import numpy as np 
import math



w,h = 500, 500


def raySegmentIntersect(ori, dir, p1, p2):

    #calculate vectors
    v1 = ori - p1
    v2 = p2 - p1
    v3 = Point(-dir.y, dir.x)

    dot = v2.dot(v3)
    
    if (abs(dot) < 0.000001 or dot == 0): #Agregué que dot no puede ser 0 para que no se produzca un error
        return [-1.0, Point(-1,-1)]

    u = v2.cross(v1) / dot
    t = v1.dot(v3) / dot

    #print(u,t)

    if (u >= 0.0 and (t >= 0.0 and t <= 1.0)):

        interX = p1.x + t*(p2.x - p1.x)
        interY = p1.y + t*(p2.y - p1.y)

        #print(interX, interY)
        
        return [u , Point(interX, interY)]

    return [-1.0, Point(-1,-1)]

def length(v1):
    #assumes v1 starts at (0,0)
    return math.sqrt(v1.x*v1.x + v1.y*v1.y)

def distanceBetweenPoints(pointA, pointB):

    return math.sqrt( (pointB.x - pointA.x)**2 + (pointB.y - pointA.y)**2 )



def normalize(v1):
    #assumes v1 starts at (0,0)
    v1 = v1 / length(v1)
    return v1

def intersectionPoint(ori, dir, dist):
    x = ori.x + dir.x*dist
    y = ori.y + dir.y*dist

    return Point(x,y)

def cosAngle(a, b, ori):
    #returns the cosine of the angle of 2 vectors that part from ori

    v1 = ori - a
    v2 = ori - b

    cos = v1.dot(v2)/(length(v1)*length(v2))
    return cos


def pendienteLinea(a, b):

    return (b.y - a.y)/(b.x - a.x)



def newDirection(point, dir, segPointA, segPointB):


    if (segPointA.x == segPointB.x): #Recta paralela al eje y, cuando no es posible calcular una pendiente

        if dir.x < 0: #Negativo

            #Viene por la derecha

            return (  normalize(Point(random.uniform(point.x + 1, w), random.uniform(0, w)) - point)  ) 


        else: 

            #Pos
            #Viene por la izquierda
            return ( normalize(Point(random.uniform(0, point.x - 1 ), random.uniform(0,w)) - point) )



    pendiente = pendienteLinea(segPointA, segPointB)

    #print(pendiente)

    if (pendiente == 0): #Recta es paralela al eje x
     

        if dir.y < 0: #Negativo

            #Viene por arriba

            return ( normalize(Point(random.uniform(0,w), random.uniform(0, point.y - 1 ))  - point ) )


        else:

            #Viene por abajo
            return ( normalize(Point(random.uniform(0,w), random.uniform(point.y + 1, w)) - point) )   

    else: #La recta no es ni vertical ni horizontal

        segmentChose = segPointB #Hay que verificar si al escoger alguno de los dos segmentos no de error

        loop = False

        while loop == False:

            randomPoint = Point( random.randint(0,w), random.randint(0,w))
    
            angulo = np.arccos( cosAngle((randomPoint - point) , segmentChose - point, point) )

            #print (randomPoint , math.degrees(angulo))

            if math.degrees(angulo) <= 90.0 and math.degrees(angulo) >= 0.0:

                return normalize(randomPoint - point)



def rayCircleIntersection ( ori, dir, posC, r):


    v1 = posC - ori #Se crea un vector con la dirección del punto aleatorio hacia el centro del círculo

    R = v1.dot(dir)/(length(dir)**2) #Punto más cercano al centro del círculo

    closest = Point(R*dir.x, R*dir.y) + ori


    b = length(posC - closest) #Distancia desde el centro al punto más cercano


    if b>r: #Si b es mayor que el radio significa que no hay intersección

        return -1


    h = math.sqrt(r*r - b*b) #uno de los catetos del triángulo

    return (R-h, R+h)  #Se retornan dos distancias



def movePoint(segPointA, segPointB, dir, point):


    if (segPointA.x == segPointB.x): #Recta paralela al eje y, cuando no es posible calcular una pendiente

        if dir.x < 0: #Negativo

            #Viene por la derecha

            point.x = point.x + 1.5

            return point


        else: 

            #Pos
            #Viene por la izquierda

            point.x = point.x - 1.5

            return point



    pendiente = pendienteLinea(segPointA, segPointB)

    #print(pendiente)

    if (pendiente == 0): #Recta es paralela al eje x
     

        if dir.y < 0: #Negativo

            #Viene por arriba

            point.y = point.y + 1.5

            return point


        else:

            #Viene por abajo
            point.y = point.y - 1.5

            return point  




def BDRF (point, dir):


    cos_theta = 0




