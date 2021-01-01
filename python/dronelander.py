#!/usr/bin/python
#Lunar lander to quad racing code. 1 motor, then two with roll. Code for simulation.
#installation
#pip install pygame

import sys
import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

#initialise pygame library
pygame.init()

#define colours
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

#set up screen size
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

"""
drawDrone Not surprisingly, it draws the drone on the screen
@param x
@param y
"""
def drawDrone(x,y):
    pts = [ (-4,-4), (-4,4), (4,4), (4,-4) ]
    verts = [ (0,1), (1,2), (2,3), (3,0) ]
    for v in verts:
        p0=(pts[v[0]][0]+x,pts[v[0]][1]+y)
        p1=(pts[v[1]][1]+x,pts[v[1]][1]+y)
        pygame.draw.line(screen,WHITE,p0,p1)
#end def

#initalise some constants
gravity = 9.81
mass = 1.0
fuel = 1000.0
maxThrust = 20.0

#initialise drone dynamics
aX=0 #acceleration in x direction
aY=0 #acceleration in y direction
vX=0 #velocity in X direction
vY=0 #velocity in Y direction
pX=SCREEN_WIDTH/2 #drone position X
pY=SCREEN_HEIGHT/2 #drone position Y


def main(args=None):
    running = True
    while running:
        # Fill the background with black
        screen.fill(BLACK)

        #control inputs

        #drone dynamics

    
        #draw instruments, fuel, vertical, horizontal

        #draw drone
        drawDrone(pX,pY)

        #double buffer flip
        pygame.display.flip()

    #endwhile running

    #tidy clean up
    pygame.quit()
#end def


#entry point
if __name__ == "__main__":
    sys.exit(main())

