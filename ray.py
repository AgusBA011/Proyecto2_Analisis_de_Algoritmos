from Point import *
import random
import numpy as np 
import math

w,h = 691, 691

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


    #print("Segmentos: ", segPointA, segPointB, "PuntoDelSalto: ", point, "Dir: ", dir)

    if (segPointA.x == segPointB.x): #Recta paralela al eje y, cuando no es posible calcular una pendiente

        if dir.x < 0: 
            #Viene por la izquierda
            
            randomPoint =  Point(random.uniform(point.x + 1, w), random.uniform(0, w))

           # print("Punto agarrado (paralela y): ", randomPoint )

            return ( randomPoint - point  ) 
        

        else: #Positivo, la x va en aumento

            #Viene por la derecha

            randomPoint =  Point(random.uniform(0, point.x - 1 ), random.uniform(0,w))

            #print("Punto agarrado (paralela y): ", randomPoint)
                        
            return ( randomPoint - point ) 



    pendiente = pendienteLinea(segPointA, segPointB)

    #print(pendiente)

    if (pendiente == 0): #Recta es paralela al eje x
     

        if dir.y < 0: #Negativo

            #Viene por arriba

            randomPoint =   Point(random.uniform(0,w), random.uniform(0, point.y - 1 ))

            #print("Punto agarrado (paralela x): ", randomPoint )

            return ( randomPoint - point )


        else:


            randomPoint =  Point(random.uniform(0,w), random.uniform(point.y + 1, w))

            #print("Punto agarrado (paralela x): ", randomPoint )

            #Viene por abajo
            return ( randomPoint - point)    

    else: #La recta no es ni vertical ni horizontal

        segmentChose = segPointB #Hay que verificar si al escoger alguno de los dos segmentos no de error

        loop = False

        while loop == False:

            randomPoint = Point( random.randint(0,w), random.randint(0,w))
    
            angulo = np.arccos( cosAngle((randomPoint - point) , segmentChose - point, point) )

            #print (randomPoint , math.degrees(angulo))

            if math.degrees(angulo) <= 90.0 and math.degrees(angulo) >= 0.0:

                return normalize(randomPoint - point)



def rayCircleIntersection ( ori, posC, r, sourcePos):


    dx = sourcePos.x - ori.x

    dy = sourcePos.y - ori.y

    A = dx * dx + dy *dy
    B = 2*(dx * (ori.x - posC.x) + dy * (ori.y - posC.y))
    C = (ori.x - posC.x) * (ori.x - posC.x) + (ori.y - posC.y) * (ori.y - posC.y) - r**2

    det = B * B -4 * A * C

    if ( A <= 0.0000001) or (det < 0):
        #Sin solu
        return -1

    elif (det == 0 ):

        #Una solu    
        t = -B / (2 * A)

        return [Point(ori.x + t * dx, ori.y + t * dy)]


    else: #Dos solus

        t = (-B + math.sqrt(det)) / (2*A)

        inter1 = Point(ori.x + t * dx, ori.y + t * dy)

        t = (-B - math.sqrt(det)) / (2*A)

        inter2 = Point(ori.x + t * dx, ori.y + t * dy)

        #print(inter1, inter2)
        return [inter1, inter2]

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

        if dir.x > 0: #Pos

            #Viene por la derecha

            point.x = point.x - 1.5

            return point


        else: 

            #Nega
            #Viene por la izquierda

            point.x = point.x + 1.5

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




def especularity (dirOfTheRay, segPointA, segPointB): #Calcular la dirección de la especularidad

    if (segPointA.x == segPointB.x): #Paralela a y

        dirOfTheRay.y = -dirOfTheRay.y

        return dirOfTheRay

    else:

        dirOfTheRay.x = -dirOfTheRay.x

        return dirOfTheRay


#print( rayCircleIntersection( Point(-2,3), Point(2,6), 4, Point(5,10)) )


#print( especularity(Point(1,-1), Point(-3,0), Point(3,0), Point(0,0))   )



'''

if (segPointA.x == segPointB.x): #Paralela a y

        if dirOfTheRay.x < 0: #Por la derecha

            vectorN = Point( w, point.y) - point

        else: #Por la izquierda

            vectorN = Point( 0, point.y) - point

    else:

        if dirOfTheRay.y < 0: #Por arriba

            vectorN = Point(point.x, 0) - point

        else:

            vectorN = Point(point.x, 500) - point

    vectorN = Point(1,0)

    #vectorN = normalize(vectorN)

    dirOfTheRay = normalize(dirOfTheRay)

    dotProduct = vectorN.dot(dirOfTheRay) 

    dotProduct = dotProduct * 2

    auxVector = Point(vectorN.x * dotProduct, vectorN.y * dotProduct)

    especularity =  dirOfTheRay - auxVector

    angulo = np.arccos( cosAngle( especularity , vectorN, point) )

    Oangulo = np.arccos( cosAngle( dirOfTheRay , vectorN, point) )

    print (math.degrees(angulo),  math.degrees(Oangulo))

'''