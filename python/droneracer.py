#!/usr/bin/python
#Drone Racing Game
#installation
#pip install pygame

import sys,math
import pygame
from pygame import surface
from pygame.locals import (
    K_UP,K_DOWN,K_LEFT,K_RIGHT,K_ESCAPE,K_SPACE,K_h,K_q,K_w,K_p,K_l,KEYDOWN,QUIT
)
from PIDController import PIDController
from coursesequencer import CourseSequencer
from colours import *
from gates import createFlag, createXGate, createGate, createTunnel, createStartFinish


#initialise pygame library
pygame.init()

#set up screen size
screenScale=100 #200
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption('Drone Racer')

#font initialisation for instruments
pygame.font.init()
FONT_SIZE = 24 #16
font = pygame.font.SysFont(pygame.font.get_default_font(), FONT_SIZE)



#initialise drone dynamics
aX=0.0 #acceleration in x direction
aY=0.0 #acceleration in y direction
vX=0.0 #velocity in X direction
vY=0.0 #velocity in Y direction
pX=SCREEN_WIDTH/2/screenScale #drone position X
pY=SCREEN_HEIGHT/screenScale #drone position Y
#angular dynamics
thetaDot=0.0 #roll acceleration
theta=0.0 #drone roll angle in rads
#and drone controls
thrust=0.0
aileron=0.0
throttle=0.0

#initalise some constants
gravity = 9.81
mass = 0.4 #1.0
Izz = 0.0012 #0.001 #roll moment of inertia
Cla = 0.8 #aileron control power (rads/sec) 0.05
Cld = 0.003 #roll drag
Cd = 0.5 #coefficient of drag
fuel = 1000.0
maxThrust = 4.5 #20.0
isAltLock = False
altLockHeight = 0


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

"""
drawWaypoint
Draws the waypoint on the screen, with the graphic reflecting the state, which
is a number representing how far it is through its animation cycle
@wayRect Rect containing the waypoint position and full size
@state number representing a size modifier 0..31 (i.e. lapTimer mod 32)
"""
def drawWaypoint(wayRect,state):
    global screen
    #pygame.draw.rect(screen,WHITE,way)
    cx=wayRect.centerx
    cy=wayRect.centery
    if (state>16):
        state = 32-state ##0..16 grows and 16..32 shrinks
    s=wayRect.width*state/48.0 #width and height the same
    pygame.draw.line(screen,YELLOW,(cx,cy+s),(cx,cy-s))
    pygame.draw.line(screen,YELLOW,(cx-s,cy),(cx+s,cy))
    pygame.draw.line(screen,YELLOW,(cx-s,cy+s),(cx+s,cy-s))
    pygame.draw.line(screen,YELLOW,(cx+s,cy+s),(cx-s,cy-s))
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
        +" t:"+'{:02.2f}'.format(throttle)
        +" vY:"+'{:02.2f}'.format(vY)
        ,True,WHITE)
    screen.blit(img,(20,20))


#end def    

################################################################################

"""
drawTiming
Draw the lap time and any other information that's useful onto the display
@lapTime The lapTimer count at 30FPS
@laps list of completed lap times, where [0]=first lap time, [1]=second lap etc
"""
def drawTiming(lapTime,laps):
    global screen,font
    #make string of previous laps
    previousTimes = ''
    for i in range(len(laps)-1,len(laps)-4,-1): #last 3 laps display
        if i>=0:
            previousTimes = previousTimes+str(i+1)+': '+'{:03.3f}'.format(laps[i])+'   '
    #end for

    #now the current time and display text
    secs = lapTime/30.0
    img = font.render(
        'Lap Time: '+'{:03.3f}'.format(secs)
        +'   '+previousTimes
        ,True,WHITE
    )
    screen.blit(img,(20,20))

################################################################################


"""
Main program and entry point
"""
def main(args=None):
    global aX,aY,vX,vY,pX,pY
    global thrust, aileron, throttle, theta, thetaDot, isAltLock, altLockHeight

    # Setup the clock for a decent framerate
    clock = pygame.time.Clock()
    lapTimer =0 #counts game loops during lap e.g. 1/30FPS
    completedLaps = [] #list of previous completed lap times
    isRaceRunning=False #flips to true when you trip the first timing gate

    heightPID = PIDController(0.4,0.025,0.35) #5,1.0,0.5 #5,0.5,0.5
    rollVelPID = PIDController(0.03,0.04,0.000005) #0.03,0.04,0.000005
    rollAnglePID = PIDController(0.06,0.01,0.005)
    throttleNudgePID = PIDController(0.4,0,0)
    aileronNudgePID = PIDController(0.1,0.02,0.005)

    #these are the bitmaps for the obstacles
    flag = createFlag()
    xGate = createXGate()
    gate = createGate()
    tunnel = createTunnel()
    startFinish = createStartFinish()
    
    course = CourseSequencer()
    #course.addWaypoint(586,175,40,0,0)
    course.addWaypoint(331,166,20,-30,0)
    course.addWaypoint(60,190,40,0,0)
    course.addWaypoint(330,298,20,0,0)
    course.addWaypoint(459,465,20,-30,0)
    course.addWaypoint(238,465,20,-30,0)
    course.addWaypoint(336,375,30,28,140) #note +100 is reversed
    course.addWaypoint(478,244,20,0,0)
    course.addWaypoint(586,175,40,0,0) #start finish
    pX=5.65 #this puts you on the grass under the start finish grid ready to go
    pY=2.38
    course.next=7 #this sets the waypoint to the start finish straight where timing starts
    running = True
    animationTimer=0
    while running:
        # Fill the background with black
        screen.fill(BLACK)
        screen.blit(flag, (80,120))
        pygame.draw.rect(screen,GREEN,(70,188,30,10))
        screen.blit(flag,(500,120))
        pygame.draw.rect(screen,GREEN,(490,188,30,10))
        pygame.draw.rect(screen,GREEN,(610,188,40,10))
        screen.blit(flag, (80,360))
        screen.blit(flag,(520,360))
        screen.blit(gate,(420,200))
        screen.blit(xGate,(224,232))
        screen.blit(gate,(180,420))
        screen.blit(gate,(400,420))
        screen.blit(tunnel,(220,130))
        screen.blit(startFinish,(534,185))

        pygame.draw.rect(screen,GREEN,(100,170,390,10))
        pygame.draw.rect(screen,GREEN,(0,306,255,10))
        pygame.draw.rect(screen,GREEN,(360,250,260,10))
        pygame.draw.rect(screen,GREEN,(0,470,640,10))
        pygame.draw.rect(screen,GREEN,(140,380,360,10)) #xgate
        

        #next waypoint
        #pygame.draw.rect(screen,WHITE,course.getNextRect())
        drawWaypoint(course.getNextRect(),animationTimer)

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
            throttle = min(throttle+0.05,1.0)
        elif keys[K_l]: #throttle down
            throttle = max(throttle-0.05,-1.0)
        else:
            throttle=0
        #use a PID to link throttle position to a desired vertical speed (vY)
        thrust = (mass*gravity) + (maxThrust/2)*throttleNudgePID.process(vY,throttle,1/30)
        thrust = max(0,thrust)
        thrust = min(maxThrust,thrust)
        ###
        if keys[K_q]: #left aileron
            aileron = max(aileron-0.05,-1.0)
        elif keys[K_w]: #right aileron
            aileron = min(aileron+0.05,1.0)
        else:
            aileron=0
        #altitude lock code
        if isAltLock:
            #thrust = mass * gravity + 10.0*(altLockHeight - pY)
            thrust = (mass*gravity) + (maxThrust/2) * heightPID.process(pY,altLockHeight,1/30)
            thrust = max(0,thrust)
            thrust = min(maxThrust,thrust)

        #drone dynamics
        #angular dynamics - version 4 angle PID control
        #a2 = rollAnglePID.process(theta,aileron*Cla,1/30)
        a2 = aileronNudgePID.process(vX,aileron*Cla,1/30)
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
        if pX<25/screenScale: #was 0
            #pX = SCREEN_WIDTH/screenScale #wrap left to right
            pX=25/screenScale
            vX=-vX
            theta=-theta
        if (pX>(SCREEN_WIDTH-25)/screenScale):
            #pX = 0 #wrap right to left
            px=(SCREEN_WIDTH-25)/screenScale
            vX=-vX
            theta=-theta
        if pY<=11/screenScale: #drone height below zero line i.e. the collision bounding box
            pY=11/screenScale
            theta = 0
            vX = 0.4 * vX
            vY = -0.4 * vY #bounce off ground! and lose some energy in the process

        #collision detection
        sX = int(pX*screenScale)
        sY = int(SCREEN_HEIGHT-pY*screenScale)
        lowPixel = screen.get_at((sX,sY+8))
        leftPixel = screen.get_at((sX-20,sY))
        rightPixel = screen.get_at((sX+20,sY))
        if lowPixel==GREEN or lowPixel==RED: #crash down
            theta = 0
            vX = 0.4 * vX
            vY = -0.4 * vY
            pY += vY*2.5/30 #stop it going through the ground
        if leftPixel==RED: #crash left (this is useful, the constant vX PID makes it spin out of control!)
            vX = -0.4 * vX
        if rightPixel==RED: #crash right
            vX = -0.4 * vX
    
        #draw instruments, fuel, vertical, horizontal
        #drawInstruments()
        drawTiming(lapTimer,completedLaps)

        #draw drone
        drawDrone(sX,sY,theta)

        #waypoint test
        (isHit, isLapComplete, jump) = course.testWaypoint(sX,sY)
        if isHit:
            pX+=jump[0]/screenScale
            pY+=jump[1]/screenScale
            isRaceRunning=True
        if isLapComplete:
            if lapTimer>1: #you get timer=1 on the initial trigger fist time you cross start - it's not a lap
                completedLaps.append(lapTimer/30.0) #log the lap time by pushing to list
                #print lap here for AI? print("lap complete: "+str(completedLaps[len(completedLaps)-1]))
            course.startLap() #and start again
            lapTimer=0

        #write out logging data
        #print(str(pY)+","+str(thrust)+","+str(altLockHeight)+","+str(aY)+","+str(vY))

        animationTimer=(animationTimer+1)%32
        if isRaceRunning:
            lapTimer+=1
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

