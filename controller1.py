# Jelani Bell-Isaac <mb0748@bard.edu>
# HW Assignment 1
# September 18th 2017

from Myro import *
from random import random
from math import *


class Controller(object):

    def __init__(self, configureBlobbing=True):
        '''Create controller for object-finding robot.'''
        # Configure blob finding settings and set IR sensor power
        if configureBlobbing:
            configureBlob(0, 200, 0, 140, 160, 254) # Configure blob YUV values
            setIRPower(160) 
        else:
            pass
        # Behaviors
        self.pushBehavior = PylonPush()
        self.avoidBehavior = Avoid()
        self.moveToPylonBehavior = MoveTowardsPylon()
        self.wanderBehavior = Wander()
        self.searchBehavior = Search()
        # Order implements priority arbitration.
        self.behaviors = [self.pushBehavior, self.moveToPylonBehavior, self.searchBehavior, self.avoidBehavior,  self.wanderBehavior]

    def arbitrate(self):
        '''Decide which behavior, in order of priority
        has a recommendation for the robot'''
        for behavior in self.behaviors:
            wantToRun = behavior.check()
            if wantToRun:
                behavior.run()
                if behavior == self.pushBehavior:
                    PylonPush.SWITCH = True
                print(getBlob())

                return 

    def run(self):
        setForwardness('fluke-forward')
        # This is the simplest loop.
        for seconds in timer(180):
            self.arbitrate()
        stop()

####################################################################################################
####################################################################################################
class Behavior(object):
    '''High level class for all behaviors.  Any behavior is a
    subclass of Behavior.'''
    SWITCH = False # A switch to determine if the robot has seen the cone and is next to it
    NO_ACTION = 0
    def __init__(self):
        # Current state of the behavior. Governs how it will respond to percepts.
        self.state = None
    def check(self):
        '''Return True if this behavior wants to execute
        Return False if it does not.'''
        return False
    def run(self):
        '''Execute whatever this behavior does.'''
        return
####################################################################################################
####################################################################################################
class PylonPush(Behavior):
    '''If the pylon is directly in front of our robot, push it forward. This is also the goal state'''

    PUSH_LEFT = 1
    PUSH_RIGHT = 2
    PUSH_STRAIGHT = 3
    PUSH_SPEED = 0.5
    PUSH_THRESH = 10000
    DSPEED = 0.1

    def __init__(self):
        '''Initializer for the Pylon push behavior'''
        self.switch = PylonPush.SWITCH
        self.state = PylonPush.NO_ACTION
        self.lspeed = PylonPush.PUSH_SPEED
        self.rspeed = PylonPush.PUSH_SPEED
    
    def check(self):
        pix, x, y = getBlob() # number of Orange pixels, the x location and the y location of the pixel's centroid
        '''Check if pylon is directly in front of robot, and to which direction to go in'''
        if pix > PUSH_THRESH:
            blobCenter = x/427 # normalize the x value
            if blobCenter < 0.2:
                self.state = PylonPush.PUSH_LEFT
            elif blobCenter > 0.8:
                self.state = PylonPush.PUSH_RIGHT
            else:
                self.state = PylonPush.PUSH_STRAIGHT
            return True
        else:
            self.state = PylonPush.NO_ACTION
            return False

    def run(self):
        '''Push the pylon towards the wall'''
        print('goal reached, PUSH')
       
        if self.state == self.PUSH_LEFT:
            self.lspeed = -self.DSPEED
            self.rspeed = self.DSPEED
        elif self.state == self.PUSH_RIGHT:
            self.lspeed = self.DSPEED
            self.rspeed = -self.DSPEED
            
        motors(self.lspeed, self.rspeed)
####################################################################################################
####################################################################################################
class Avoid(Behavior):
    '''Behavior to avoid obstacles.  Simply turns away.'''
    
    TURN_LEFT = 1
    TURN_RIGHT = 2
    TURN_SPEED = 1
    TURN_DURATION = 0.25
    OBSTACLE_THRESH = 1000


    def __init__(self):
        '''Initializer for the Avoid behavior'''
        self.state = Avoid.NO_ACTION
        self.turnspeed = Avoid.TURN_SPEED
        self.turndur = Avoid.TURN_DURATION

    def check(self):
        '''see if there are any obstacles.  If so turn other direction'''
        L, C, R = getObstacle() # Left, Center, Right IR values

        if L > self.OBSTACLE_THRESH:
            self.state = Avoid.TURN_RIGHT
            return True
        elif R > self.OBSTACLE_THRESH:
            self.state = Avoid.TURN_LEFT           
            return True
        elif (L+C+R)/3.0 > self.OBSTACLE_THRESH:              
            self.state = Avoid.TURN_LEFT
            return True
        else:
            self.state = Avoid.NO_ACTION
            return False

    def run(self):
        '''see if there are any obstacles.  If so turn other direction'''
        print("Avoid")
        if self.state == Avoid.TURN_RIGHT:
            print('turning right')
            turnRight(self.turnspeed, self.turndur)
        elif self.state == Avoid.TURN_LEFT:
            print('turning left')
            turnLeft(self.turnspeed, self.turndur)
####################################################################################################
####################################################################################################
class MoveTowardsPylon(Behavior):
    '''If the cone has been detected, move towards it'''

    ATTACK_LEFT = 1
    ATTACK_RIGHT = 2
    ATTACK_STRAIGHT = 3
    ATTACK_SPEED = .3
    ATTACK_THRESH = 2000
    TDUR = 0.2
    

    def __init__(self):
        '''Initializer for the Pylon attack behavior'''
        self.state = MoveTowardsPylon.NO_ACTION
        self.lSpeed = MoveTowardsPylon.ATTACK_SPEED
        self.rSpeed = MoveTowardsPylon.ATTACK_SPEED
        self.turnDuration = MoveTowardsPylon.TDUR

    def check(self):
        pix, x, y = getBlob()
        '''Check if the Pylon has been detected'''
        blobCenter = x/427 # normalize the x value

        if pix > ATTACK_THRESH: 
                print("Cone is at ", x)

                if blobCenter < 0.3:
                    self.state = self.ATTACK_LEFT
                elif blobCenter > 0.6:
                    self.state = self.ATTACK_RIGHT
                else:
                    self.state = self.ATTACK_STRAIGHT
                return True
        else:
                self.state = self.NO_ACTION
                return False
            
    
    def run(self):
        '''If the pylon is in view, drive towards it while adjusting for where the blob is on screen'''
        print('attack')
        if self.state == self.ATTACK_LEFT:
            turnLeft(self.lSpeed, self.turnDuration)
        elif self.state == self.ATTACK_RIGHT:
            turnRight(rSpeed, self.turnDuration)    
        else:
            forward(1)    
####################################################################################################
####################################################################################################
class Wander(Behavior):
    '''Behavior to wander forward. Heads in direction that varies a bit each time it executes.'''

    WANDER = 1
    OBSTACLE_THRESH = 3000
    MAX_SPEED = 1.0
    MIN_SPEED = 0.1
    DSPEED_MAX = 0.1 # most speed can change on one call

    def __init__(self):
        '''Initializer for the Wander behavior'''
        self.state = Wander.NO_ACTION
        self.lspeed = self.MAX_SPEED # speed of left motor
        self.rspeed = self.MAX_SPEED # speed of right motor

    def check(self):
        '''see if there are any possible obstacles.  If not, then wander.'''
        L, C, R = getObstacle()        
        if (L+C+R)/3.0 < self.OBSTACLE_THRESH:
            self.state = self.WANDER
            return True
        elif getStall() == 1: # If stalled, backup
            print("Stalled")
            backward(self.MAX_SPEED, 1)
        else:
            self.state = self.NO_ACTION
            return False

    def run(self):
        '''Modify current motor commands by a value in range [-0.25,0.25].'''
        print("Wander")
        dl = (2 * random() - 1) * self.DSPEED_MAX
        dr = (2 * random() - 1) * self.DSPEED_MAX
        self.lspeed = max(self.MIN_SPEED,min(self.MAX_SPEED,self.lspeed+dl))
        self.rspeed = max(self.MIN_SPEED,min(self.MAX_SPEED,self.rspeed+dr))
        motors(self.lspeed,self.rspeed)
       
####################################################################################################
####################################################################################################
class Search(Behavior):
    '''Behavior to search after the pylon has been pushed and the robot no onger sees it.'''

    SEARCH = 1
    SEARCH_SPEED = 0.5
    DSPEED_MAX = 0.1 # most speed can change on one call

    def __init__(self):
        self.state = Search.NO_ACTION

    def check(self):
        if PylonPush.SWITCH == True: # Check switch, don't leave the cone
            self.state = self.SEARCH
            return True
        else:
            self.state = self.NO_ACTION
            return False

    def run(self):
        if self.state == self.SEARCH:
            print("Searching...")
            turnLeft(SEARCH_SPEED, 1)
            motors(0,0)
            
###################################################################################################


if __name__ == "__main__":
    ctl = Controller()
    ctl.run()