#!/usr/bin/python
#Lunar lander to quad racing code. 1 motor, then two with roll. Code for simulation.
#installation
#pip install pygame

import sys,math
import pygame
from pygame.locals import (
    K_UP,K_DOWN,K_LEFT,K_RIGHT,K_ESCAPE,K_SPACE,K_h,K_q,K_w,K_p,K_l,KEYDOWN,QUIT
)
from PIDController import PIDController

#initialise pygame library
pygame.init()

#set up screen size
screenScale=100 #200
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption('Drone Lander')

#font initialisation for instruments
pygame.font.init()
font = pygame.font.SysFont(pygame.font.get_default_font(), 16)


#define colours
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)


#initialise drone dynamics
aX=0.0 #acceleration in x direction
aY=0.0 #acceleration in y direction
vX=0.0 #velocity in X direction
vY=0.0 #velocity in Y direction
#vX=0.0 #velocity earth axes
#vY=0.0 #velocity earth axes
pX=SCREEN_WIDTH/2/screenScale #drone position X
pY=SCREEN_HEIGHT/screenScale #drone position Y
#angular dynamics
p=0.0 #roll rate
thetaDot=0.0 #roll acceleration
theta=0.0 #drone roll angle in rads
#and drone controls
thrust=0.0
aileron=0.0

#initalise some constants
gravity = 9.81
mass = 0.4 #1.0
Izz = 0.0012 #0.001 #roll moment of inertia
Cla = 1.5 #aileron control power (rads/sec) 0.05
Cld = 0.003 #roll drag
Cd = 0.25 #coefficient of drag
fuel = 1000.0
maxThrust = 4.5 #20.0
isAltLock = False
altLockHeight = 0

#PIDControllers
#heightPID = PIDController(1.0,0,0) #do i need this?

################################################################################

"""
drawDrone Not surprisingly, it draws the drone on the screen
@param x
@param y
@param a Drone rotation (radians), positive is right roll
"""
def drawDrone(x,y,a):
    pts = [
        (-9,1), (-9,2), (9,2), (9,1), #central slice
        (-7,-4), (-4,0), (-3,1), (3,1), (4,0), (7,-4), (2,0), (-2,0), #feet
        (-2,2), (-1,3), (1,3), (2,2), #top
        (-3,6), (3,6), #antennae
        (-11,1), (-11,4), (-9,4), #l motor
        (9,4), (11,4), (11,1), #r motor
        (-14,5), (-10,5), (-6,5), #l prop
        (6,5), (10,5), (14,5) #r prop
    ]
    verts = [
        (1,2), (0,3), #central slice
        (4,5), (5,6), (11,4), # l leg
        (7,8), (8,9), (9,10), (10,11), #r leg
        (12,13), (13,14), (14,15), #top
        (13,16), # l antenna
        (14,17), # r anetnna
        (18,19), (19,20), (20,0), (0,18), # l motor
        (3,21), (21,22), (22,23), (23,3), #r motor
        (24,25), (25,26), #l props
        (27,28), (28,29) #r props
    ]
    #rotation
    for i in range(0,len(pts)):
        x1=float(pts[i][0])
        y1=float(pts[i][1])
        x2 = x1*math.cos(a) + y1*math.sin(a)
        y2 = y1*math.cos(a) - x1*math.sin(a)
        pts[i]=(x2,y2)
    #drawing
    s=screenScale/100
    for v in verts:
        p0=(s*pts[v[0]][0]+x,y-s*pts[v[0]][1])
        p1=(s*pts[v[1]][0]+x,y-s*pts[v[1]][1])
        pygame.draw.line(screen,WHITE,p0,p1)
    #todo: animate the props on alternate frame cycles
#end def

################################################################################

def drawInstruments():
    global screen, font, pX, pY, altLockHeight
    img = font.render(
        "Px:"+'{:02.2f}'.format(pX)
        +" Py:"+'{:02.2f}'.format(pY)
        +" T:"+'{:02.2f}'.format(thrust)
        +" lock:"+str(altLockHeight)
        +" a:"+'{:02.2f}'.format(aileron*Cla)
        +" tDot:"+'{:02.2f}'.format(thetaDot)
        +" t:"+'{:02.2f}'.format(theta)
        ,True,WHITE)
    screen.blit(img,(20,20))


#end def    

################################################################################


"""
Main program and entry point
"""
def main(args=None):
    global aX,aY,vX,vY,pX,pY
    global thrust, aileron, theta, thetaDot, p, isAltLock, altLockHeight

    # Setup the clock for a decent framerate
    clock = pygame.time.Clock()

    heightPID = PIDController(0.4,0.025,0.35) #5,1.0,0.5 #5,0.5,0.5
    rollVelPID = PIDController(0.03,0.04,0.000005) #0.03,0.04,0.000005
    rollAnglePID = PIDController(0.06,0.01,0.005)
    
    running = True
    while running:
        # Fill the background with black
        screen.fill(BLACK)

        #control inputs
        for event in pygame.event.get():
            if event.type==QUIT:
                running=False
            elif event.type==KEYDOWN:
                #if event.key==K_LEFT:
                #if event.key==K_RIGHT:
                #if event.key==K_UP:
                #if event.key==K_DOWN:
                if event.key==K_ESCAPE:
                    running=False
                elif event.key==K_h:
                    altLockHeight=pY
                    isAltLock=not isAltLock
            #end if
        #end for
        #if you're pressing SPACE increase the thrust, otherwise decrease the thrust
        keys = pygame.key.get_pressed()
        if keys[K_p]: #throttle up
            thrust+=0.05
            if thrust>maxThrust:
                thrust = maxThrust
        if keys[K_l]: #throttle down
            thrust-=0.05
            if (thrust<0):
                thrust=0
        if keys[K_q]: #left aileron
            aileron = max(aileron-0.05,-1.0)
        if keys[K_w]: #right aileron
            aileron = min(aileron+0.05,1.0)
        #altitude lock code
        if isAltLock:
            #thrust = mass * gravity + 10.0*(altLockHeight - pY)
            thrust = (mass*gravity) + (maxThrust/2) * heightPID.process(pY,altLockHeight,1/30)
            thrust = max(0,thrust)
            thrust = min(maxThrust,thrust)      

        #drone dynamics
        #angular dynamics - version 1 direct control
        #theta=aileron
        ###
        #angular dynamics - version 2 acceleration control
        #L = aileron * Cla - Cld*thetaDot #roll power (torque) minus drag
        #pDot = L / Izz #A=F/m
        #thetaDot = pDot*(1.0/30.0) #integrate pDot to get p, which is thetaDot
        #theta+=thetaDot*(1.0/30.0)
        ###
        #angular dynamics - version 3 velocity PID control
        #a2 = rollVelPID.process(thetaDot,aileron*Cla,1/30)
        #L = a2 - Cld*thetaDot #L (torque) = roll power (torque) minus drag
        #pDot = L / Izz #A=F/m
        #thetaDot = pDot*(1.0/30.0) #integrate pDot to get p, which is thetaDot
        #theta+=thetaDot*(1.0/30.0)
        ###
        #angular dynamics - version 4 angle PID control
        a2 = rollAnglePID.process(theta,aileron*Cla,1/30)
        L = a2 - Cld*thetaDot #L (torque) = roll power (torque) minus drag
        pDot = L / Izz #A=F/m
        thetaDot = pDot*(1.0/30.0) #integrate pDot to get p, which is thetaDot
        theta+=thetaDot*(1.0/30.0)

        #speed and drag
        vsq = vX*vX+vY*vY
        if (vsq>0):
            v = math.sqrt(vsq)
            dx = vX/v
            dy = vY/v
        else:
            v=0
            dx=0
            dy=0
        fX = thrust * math.sin(theta) - Cd*vsq*dx #force +ve=right
        fY = -mass*gravity + thrust * math.cos(theta) - Cd*vsq*dy #force +ve=up
        #acceleration and velocity
        aX = fX/mass
        aY = fY/mass #F=ma, a=F/m
        vX+= aX*(1.0/30.0)
        vY+= aY*(1.0/30.0)
        #update position
        pX+= vX*(1.0/30.0)
        pY+= vY*(1.0/30.0) #30 FPS, 1 pixel per metre
        if pX<0:
            pX = SCREEN_WIDTH/screenScale #wrap left to right
        if (pX>SCREEN_WIDTH/screenScale):
            pX = 0 #wrap right to left
        if pY<=11/screenScale: #drone height below zero line i.e. the collision bounding box
            pY=11/screenScale
            theta = 0
            vX = 0.4 * vX
            vY = -0.4 * vY #bounce off ground! and lose some energy in the process

    
        #draw instruments, fuel, vertical, horizontal
        drawInstruments()

        #draw drone
        drawDrone(pX*screenScale,SCREEN_HEIGHT-pY*screenScale,theta)

        #write out logging data
        #print(str(pY)+","+str(thrust)+","+str(altLockHeight)+","+str(aY)+","+str(vY))

        #double buffer flip
        pygame.display.flip()
        # Ensure program maintains a rate of 30 frames per second
        clock.tick(30)

    #endwhile running

    #exit gracefully, shutting down the pygame system cleanly
    pygame.quit()
#end def

################################################################################

#entry point
if __name__ == "__main__":
    sys.exit(main())

