"""
gates.py
Drawing functions for making the gates in the droneracer.py
"""

import pygame
from pygame import surface
from colours import *


################################################################################

"""
createFlag Draw a flag a to a surface and return
"""
def createFlag():
    s=3
    surface = pygame.Surface((6*s,23*s))
    #pygame.draw.aalines(surface,WHITE,True,[(0*s,22*s),(2*s,20*s),(4*s,22*s)]) #base tri
    pygame.draw.polygon(surface,WHITE,[(0*s,22*s),(2*s,20*s),(4*s,22*s)]) #solid base tri
    pygame.draw.polygon(surface,WHITE,[(2*s,0*s),(5*s,2*s),(5*s,12*s),(2*s,18*s)]) #solid body
    pygame.draw.polygon(surface,RED,[(2*s,4*s),(2*s,0*s),(5*s,2*s)])#top tri
    pygame.draw.polygon(surface,RED,[(2*s,8*s),(2*s,4*s),(5*s,6*s)])#mid tri
    pygame.draw.polygon(surface,RED,[(2*s,12*s),(2*s,8*s),(5*s,10*s)])#bottom tri
    pygame.draw.aalines(surface,WHITE,False,[(2*s,20*s),(2*s,0*s),(5*s,2*s),(5*s,12*s),(2*s,18*s)])#outline
    
    return surface
#end def

################################################################################

"""
createXGate Draw the big cross (X) triangle gate
"""
def createXGate():
    s=6
    surface = pygame.Surface((32*s,24*s))
    #left leg
    pygame.draw.polygon(surface,WHITE,[
        (0*s,24*s), (4*s,18*s), (10*s,18*s), (6*s,24*s)
    ])
    #left upper
    pygame.draw.polygon(surface,RED,[
        (4*s,18*s), (8*s,12*s), (16*s,12*s), (16*s,16*s), (10*s,18*s)
    ])
    #right leg
    pygame.draw.polygon(surface,WHITE,[
        (32*s,24*s), (26*s,24*s), (22*s,18*s), (28*s,18*s)
    ])
    #right upper
    pygame.draw.polygon(surface,RED,[
        (28*s,18*s), (22*s,18*s), (16*s,16*s), (16*s,12*s), (24*s,12*s)
    ])

    #base left
    #pygame.draw.polygon(surface,WHITE,[
    #    (0*s,24*s), (8*s,12*s), (16*s,12*s), 
    #    (16*s,16*s), (10*s,18*s), (6*s,24*s)])
    #base right
    #pygame.draw.polygon(surface,WHITE,[
    #    (16*s,12*s), (24*s,12*s), (32*s,24*s),
    #    (26*s,24*s), (22*s,18*s), (16*s,16*s)
    #])
    #top tri
    pygame.draw.polygon(surface,RED,[(12*s,6*s), (16*s,0*s), (20*s,6*s)])
    return surface
#end def

################################################################################

"""
createGate Draw the regular gate
"""
def createGate():
    s=6
    surface = pygame.Surface((16*s,8*s))
    #left
    pygame.draw.polygon(surface,WHITE,[
        (0*s,8*s), (0*s,4*s), (2*s,2*s), (6*s,0*s), (8*s,0*s), (8*s,2*s),
        (4*s,3*s), (2*s,5*s), (2*s,8*s)
    ])
    #right
    pygame.draw.polygon(surface,WHITE,[
        (8*s,0*s), (10*s,0*s), (14*s,2*s), (16*s,4*s), (16*s,8*s),
        (14*s,8*s), (14*s,5*s), (12*s,3*s), (8*s,2*s)
    ])
    #TODO: coloured triangle bits here
    #centre
    pygame.draw.polygon(surface,RED,[
        (8*s,1.5*s), (6.5*s,0.5*s), (9.5*s,0.5*s)
    ])
    #left
    pygame.draw.polygon(surface,MAGENTA,[
        (3*s,2*s), (6*s,0.5*s), (5.5*s,2*s)
    ])
    #right
    pygame.draw.polygon(surface,MAGENTA,[
        (13*s,2*s), (10*s,0.5*s), (10.5*s,2*s)
    ])
    #further left
    pygame.draw.polygon(surface,MAGENTA,[
        (2.5*s,4*s), (2.5*s,2.5*s), (1*s,4*s)
    ])
    #further right
    pygame.draw.polygon(surface,MAGENTA,[
        (13.5*s,4*s), (13.5*s,2.5*s), (15*s,4*s)
    ])
    #left vertical
    pygame.draw.polygon(surface,MAGENTA,[
        (1.5*s,6*s), (0.5*s,7*s), (0.5*s,5*s)
    ])
    #right vertical
    pygame.draw.polygon(surface,MAGENTA,[
        (14.5*s,6*s), (15.5*s,7*s), (15.5*s,5*s)
    ])
    return surface
#end def

################################################################################

"""
createTunnel Draw the tunnel graphic
"""
def createTunnel():
    s=4
    surface = pygame.Surface((35*s,10*s))
    #tunnel
    pygame.draw.polygon(surface,WHITE,[
        (0*s,10*s), (0*s,2*s), (19*s,2*s), (17*s,4*s), (17*s,10*s)   
    ])
    #red
    pygame.draw.polygon(surface,RED,[
        (0*s,0*s), (23*s,0*s), (19*s,2*s), (0*s,2*s)
    ])
    #opening left
    pygame.draw.polygon(surface,MAGENTA,[
        (17*s,10*s), (17*s,4*s), (19*s,2*s), (23*s,0*s), (25*s,0*s),
        (25*s,2*s), (19*s,5*s), (19*s,10*s)
    ])
    #opening right
    pygame.draw.polygon(surface,MAGENTA,[
        (25*s,0*s), (27*s,0*s), (31*s,2*s), (33*s,4*s), (33*s,10*s),
        (31*s,10*s), (31*s,5*s), (25*s,2*s)
    ])
    return surface
#end def

################################################################################

"""
Create start finish line chequered pattern (horizontal)
"""
def createStartFinish():
    s=2
    size=4 #size of square, where spacing between same colours is spacing*2
    surface = pygame.Surface((32*s,8*s))
    pygame.draw.polygon(surface,WHITE,[
        (0*s,0*s), (32*s,0*s), (32*s,8*s), (0*s,8*s)
    ])
    for x in range(0,4): #count of how many coloured squares fit in 32 pixels i.e. 32/(size*2)
        x1=s*x*size*2
        x2=s*(x*size*2+size)
        y1=0*s
        y2=size*s
        dx=size*s #offset for bottom row
        #top line
        pygame.draw.polygon(surface,MAGENTA,[
            (x1,y1), (x2,y1), (x2,y2), (x1,y2)
        ])
        #bottom line x offset
        pygame.draw.polygon(surface,MAGENTA,[
            (x1+dx,y1+dx), (x2+dx,y1+dx), (x2+dx,y1+2*dx), (x1+dx,y1+2*dx)
        ])
    return surface
#end def