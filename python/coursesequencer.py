"""
coursesequencer.py
Used with dronelander.py to set the sequence of gates needed to fly
through in order to complete the course.
"""

import pygame

class CourseSequencer:
    def __init__(self):
        self.sequence = [] #Rect objects
        self.jumps = [] #(x,y) tuples, added to drone xy coords when gate passed
        self.next = 0 #which one is the next gate in the sequence
 
    #end def

    ################################################################################

    """
    start
    Reset the sequence to the start and begin timing the lap (TODO)
    """
    def startLap(self):
        self.next=0
    #end def

    ################################################################################

    """
    addWaypoint Adds a waypoint to the end of the current course sequence
    @param x Centre X coordinate of the position the drone has to fly to
    @param y Centre Y
    @param size Size of the target box that the drone centre must be inside
    to trigger this waypoint as hit and move on to the next. The size is the
    length in pixels from the centre X,Y to the top left i.e. half the side
    length
    @param jumpx x coord to get added to the drone's x coord when gate is traversed (i.e. a jump)
                    NOTE: jump coords are in PIXELS, not metres - main program does conversion.
    @param jumpy same as jumpx, but for y coord
    """
    def addWaypoint(self,x,y,size,jumpx,jumpy):
        #self.sequence.append((x,y,size))
        self.sequence.append(pygame.Rect(x-size,y-size,size,size))
        self.jumps.append((jumpx,jumpy))
    #end def

    #addWaypoints

    ################################################################################

    """
    testWaypoint
    Test for the drone intersecting the the next current waypoint in the sequence
    @param x X coord of drone
    @param y Y coord of drone
    @returns (isHit, isLapComplete, jump) where isHit means the next waypoint was completed
    as the drone xy hit the rect, then isLapComplete if it was the last in the sequence
    and the lap is complete. Jump is the offset to add to the drone after traversing the
    obstacle.
    """
    def testWaypoint(self,x,y):
        isLapComplete = False
        isHit = self.sequence[self.next].collidepoint(x,y)
        jump = ()
        if isHit:
            jump = self.jumps[self.next]
            self.next+=1
            if self.next>=len(self.sequence):
                isLapComplete=True
                #self.startLap() # no, let the main program do it
            #end if
        #end if
        return (isHit, isLapComplete, jump)
    #end def

    ################################################################################

    """
    getNextRect
    Used by the main program rendering to get the rect containing the drone's next
    waypoint in the sequence so that it can be drawn on the screen to show the
    player where to go next.
    """
    def getNextRect(self):
        return self.sequence[self.next]
    #end def
    
    ################################################################################
