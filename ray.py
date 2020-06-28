from Point import *
import math

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

