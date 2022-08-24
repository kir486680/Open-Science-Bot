import os 
import math 
from mindstorms import Motor, Hub
import time
from ComArduino import LiquidHandler
import numpy as np

hub = Hub()
time.sleep(1)
class Arm:
    def __init__(self):
        self.gripper = hub.port.D.motor
        self.arm = hub.port.B.motor #the highest it goes is  -120
        self.gripperPos = 0
        self.armPos = 0
        
    def setDefault(self):
        #while not self.arm.was_stalled():
            #self.arm.start(50)
        self.arm.set_degrees_counted(0)
        self.updateCurrentPosition()
    def moveDown(self): # the desired delta is 350
        #self.arm.run_to_position(180, 'counterclockwise', 30) #-400 acceptable
        self.arm.run_for_degrees(220, speed=-30)
        #self.updateCurrentPosition() 
    def moveLower(self): # the desired delta is 350
        #self.arm.run_to_position(180, 'counterclockwise', 30) #-400 acceptable
        self.arm.run_for_degrees(350, speed=-30)
        #self.updateCurrentPosition() 
    def moveUp(self):
      
        #self.arm.run_to_degrees_counted(45,30) 
        self.arm.run_for_degrees(-225, speed=30)
        #self.arm.run_to_degrees_counted(0,30)
        #self.updateCurrentPosition()
    def moveTo(self,x):
        self.arm.run_to_degrees_counted(x,30)
        #self.arm.run_to_degrees_counted(0,30)
        self.updateCurrentPosition()
    def grip(self):#delta is -10
        #self.gripper.run_to_position(78,speed=50)
        self.gripper.run_for_degrees(30,30)
        #self.updateCurrentPosition()
    def release(self):
        #self.gripper.run_to_position(93,speed=50)
        self.gripper.run_for_degrees(-30,-30)
        #self.updateCurrentPosition()
    def releaseIntoBeaker(self):
        #self.gripper.run_to_position(205,speed=50)
        self.gripper.run_to_degrees_counted(25,30)
        self.updateCurrentPosition()
    def updateCurrentPosition(self):
        abs_pos = self.arm.get_position() 
        self.armPos = abs_pos
        print("Updated Arm position to: " + str(abs_pos))
        abs_pos = self.gripper.get_position()
        self.gripperPos = abs_pos
        print("Updated Gripper position to: " + str(abs_pos))
    def getCurrentPosition(self):
        print("Absolute Gripper Position: " + str(self.gripperPos))
        print("Absolute Arm Position: " + str(self.armPos))



class Base:
    def __init__(self):
        self.wheels = hub.port.E.motor
        self.wheelsPos = 0
        
    def setDefault(self):
        self.wheels.preset(self.wheels.get()[0])
    def moveForward(self):
        self.wheels.run_to_position(-1200,speed=50)
    def moveBackwards(self):
        self.wheels.run_to_position(0,speed=50)
    def moveToOrigin(self):
        self.wheels.run_to_position(0, speed=50)
    def presetOrigin(self):
        self.wheels.preset(self.wheels.get()[0])
    def moveTo(self, x):
        self.wheels.run_to_position(x,speed=50)
    def updateCurrentPosition(self):
        while self.wheels.busy(1):
            time.sleep(10)
        abs_pos = self.wheels.getPosition()
        print("Absolute Wheels position: " + str(abs_pos))
    def getCurrentPosition(self):
        print("Absolurte Wheels position " + str(self.wheelsPos))


class Board():
    def __init__(self, arm, base):
        
        self.arms = arm
        self.base = base
        self.peripherals = []
    def status(self):
        self.arms.getCurrentPosition()
        self.base.getCurrentPosition()
    def load_labwear(self, name, locationStart=0, numLots = 3, lotSize = 300, taken = [0,0,0],size = 0):
    #fix this the following way https://stackoverflow.com/questions/5079609/methods-with-the-same-name-in-one-class-in-python
        if name == 'MetalHolder':
            metalHolder = self.MetalHolder(locationStart, numLots, taken = taken, lotSize = -lotSize) # generate an empty array of 0 be default
            self.peripherals.append(metalHolder)
        if name == 'Beaker':
            beaker = self.Beaker(size, locationStart)
            self.peripherals.append(beaker)

    def encoder(self):
        #assume that first is the metal holder, second beaker, and third metal holder
        metalHolder1 = self.peripherals[0]
        beaker = self.peripherals[1]
        metalHolder2 = self.peripherals[2]
        #check if there is enough space for metal pieces from holder1 in holder2 
        if np.count_nonzero(metalHolder1.taken) <= np.count_nonzero(np.array(metalHolder2.taken)==0):
            for i in range(np.count_nonzero(metalHolder1.taken)):
                
                while True:
                    lotIdx1 = metalHolder1.findTaken()
                    lotIdx2 = metalHolder2.findFreeLot()
                    if lotIdx1 is not None and lotIdx2 is not None:
                        self.base.moveTo(lotIdx1) 
                        time.sleep(2)
                        self.arms.moveDown() 
                        time.sleep(2)
                        self.arms.grip()
                        time.sleep(2)
                        self.arms.moveUp()
                        time.sleep(2)
                         #end of pickup 
                        #moving to the beaker
                        
                        self.base.moveTo(beaker.start)
                        time.sleep(2)
                        self.arms.moveDown()
                        #Water logic should be performed here
                        time.sleep(2)
                        self.arms.moveUp()
                        time.sleep(2)
                        #end of beakerDip
                        #this is always true for releaseing 1 part 

                        self.base.moveTo(lotIdx2) 
                        time.sleep(2)
                        self.arms.moveDown() 
                        time.sleep(2)
                        self.arms.release()
                        time.sleep(2)
                        self.arms.moveUp()
                        time.sleep(2)
                        #end of release
        else:
            print("The number of metals you are trying to transport is too big")

    class Beaker():
        sizeOptions = [[30,40], [50,60]] #comes in as [height, radius]
        def __init__(self, size, location):
            self.size = self.sizeOptions[size]
            self.start = location
            self.end = location +size
        def changeSize(size):
            self.size = self.sizeOptions[size]


    class MetalHolder():

        
        def __init__(self, locationStart, numLots, taken, lotSize = -300):
            self.start = locationStart
            self.numLots = numLots
            self.lotSize = lotSize
            self.coordinates = []
            self.generateLocation(locationStart) # array of x and y coordiates of the spots in the holder
            self.taken = taken # array of taken spots of the holder
          

        def updateLot(self, idx, status=1):
            self.taken[idx] = status
        def status(self):
            for x,status in zip([x for x,y in self.coordinates], self.taken):
                print("The point with coordinates " + str(x) + " has status " + str(status))
        #Finds the part where there is no metal piece and swtiches it to taken
        def findFreeLot(self):
            for count, coord in enumerate(self.coordinates):
                print(count)
                print(self.taken)
                if not self.taken[count]:
                    x, y = coord
                    self.updateLot(count)
                    return x
            return None
        #Finds the part where there is already a metal piece and switeches it to free
        def findTaken(self):
            for count, coord in enumerate(self.coordinates):
                if self.taken[count]:
                    x, y = coord
                    self.updateLot(count,0)
                    return x
            return None
        def generateLocation(self, start):            
            y = 0
            x = start
            self.coordinates.append([x,y])
            for i in range(self.numLots-1):
                x += self.lotSize
                self.coordinates.append([x,y])
            print(self.coordinates)

            
arms = Arm()
base = Base()
board = Board(arms, base)
#liquid = LiquidHandler('COM3',9600)


#testData.append("<2,20,1>")
board.load_labwear('MetalHolder', taken = [1,1,0])
board.load_labwear('Beaker', size = 1, locationStart = -1400)
board.load_labwear('MetalHolder', locationStart = -2000)
#print(board.peripherals[0].coordinates)
#board.performExperiment("fdf")

#board.encoder()
#arms.setDefault()

debug = False
def dist2deg(desiredDistance, diameter):
    distancePerDegree = np.pi * diameter / 360
    return desiredDistance/distancePerDegree

def dist2deg2(desiredDistance):
    return desiredDistance/0.02666667


if debug ==False:
    wheels_x = hub.port.E.motor
    wheels_y = hub.port.A.motor
    metalSamples = [[0.0,0.0],[0.0,3.4], [0.0,6.8]]
    beaker1 = (7.5,0.4)
    beaker2 = (7.5,8.2)
    beaker3 = (15,4.5)
    curX = 0.0
    curY = 0.0
    def rotate(currentY, targetY, diam):
        dist = dist2deg(math.dist([targetY], [currentY]),4.2)
        if  targetY-currentY< 0:
            
            wheels_y.run_for_degrees(dist, 30) 
        else:
            wheels_y.run_for_degrees(-dist, -30) 
    for metalX, metalY in metalSamples:

        dist = dist2deg(metalX-curX,1.3)
        wheels_x.run_for_degrees(dist, 30)  
        rotate(curY, metalY, 4.2)
        curX += metalX-curX
        curY += metalY-curY
        print(curX, curY)
        time.sleep(6)
        #arms.moveDown()
        #time.sleep(2)
        #arms.grip()
        #time.sleep(2)
        #arms.moveUp()
        #time.sleep(2)
        
        dist = dist2deg(beaker1[0]-curX,1.3)
        wheels_x.run_for_degrees(dist, -30)  
        rotate(curY, beaker1[1], 4.2)
        curX += beaker1[0]-curX
        curY += beaker1[1]-curY
        print(curX, curY)
        time.sleep(6)
        #time.sleep(2)
        #arms.moveDown()
        #time.sleep(2)
        #arms.moveUp()
        #time.sleep(2)
        


        rotate(curY, beaker2[1], 4.2)
        curY += beaker2[1]-curY
        print(curX, curY)
        time.sleep(6)
        #time.sleep(2)
        #arms.moveDown()
        #time.sleep(2)
        #arms.moveUp()
        #time.sleep(2)
        

        dist = dist2deg(beaker3[0]-curX,1.3)
        wheels_x.run_for_degrees(dist, -30)
        rotate(curY, beaker3[1], 4.2)
        curX += beaker3[0]-curX
        curY += beaker3[1]-curY
        print(curX, curY)
        time.sleep(6)
        #time.sleep(2)
        #arms.moveDown()
        #time.sleep(2)
        #arms.moveUp()
        #time.sleep(2)  
   


    """
    curX = 0
    curY = 0
    
    beaker1 = (7.5,0.4)
    beaker2 = (7.5,8.2)
    beaker3 = (15,4.5)
    metalSample2 = (0,3.4)
    

    arms.moveDown()
    time.sleep(2)
    arms.grip()
    time.sleep(2)
    arms.moveUp()
    time.sleep(2)


    dist = dist2deg(beaker1[0]-curX,1.3)
    wheels_x = hub.port.E.motor
    wheels_x.run_for_degrees(dist, -30)
    dist = dist2deg(beaker1[1]-curY,4.2)
    wheels_y = hub.port.A.motor
    wheels_y.run_for_degrees(dist, -30)
    curX = beaker1[0]-curX
    curY = beaker1[1]-curY
    time.sleep(2)
    arms.moveDown()
    time.sleep(2)
    arms.moveUp()
    time.sleep(2)
    


    dist = dist2deg(beaker2[1]-curY,4.2)
    wheels_y.run_for_degrees(dist, -30)
    curY += beaker2[1]-curY
    time.sleep(2)
    arms.moveDown()
    time.sleep(2)
    arms.moveUp()
    time.sleep(2)
    

    dist = dist2deg(beaker3[0]-curX,1.3)
    wheels_x.run_for_degrees(dist, -30)
    dist = dist2deg(beaker3[1]-curY,4.2)
    wheels_y.run_for_degrees(dist, 30)
    curX += beaker3[0]-curX
    curY += beaker3[1]-curY
    time.sleep(2)
    arms.moveDown()
    time.sleep(2)
    arms.moveUp()
    time.sleep(2)


    arms.release()
    print(curX)
    print(curY)
    """
    """

    dist = dist2deg(metalSample2[0]-curX,1.3)
    wheels_x = hub.port.E.motor
    wheels_x.run_for_degrees(dist, 30)  #Important to be positive!
    dist = dist2deg(metalSample2[1]-curY,4.2)
    wheels_y = hub.port.A.motor
    wheels_y.run_for_degrees(dist, 30)
    curX += metalSample2[0]-curX
    curY += metalSample2[1]-curY
    print(curX, curY)
    time.sleep(6)
    #arms.moveDown()
    #time.sleep(2)
    #arms.grip()
    #time.sleep(2)
    #arms.moveUp()
    #time.sleep(2)
    
    dist = dist2deg(beaker1[0]-curX,1.3)
    wheels_x = hub.port.E.motor
    wheels_x.run_for_degrees(dist, -30)
    dist = dist2deg(beaker1[1]-curY,4.2)
    wheels_y = hub.port.A.motor
    wheels_y.run_for_degrees(dist, 30)
    curX += beaker1[0]-curX
    curY += beaker1[1]-curY
    print(curX, curY)
    time.sleep(6)
    #time.sleep(2)
    #arms.moveDown()
    #time.sleep(2)
    #arms.moveUp()
    #time.sleep(2)
    


    dist = dist2deg(beaker2[1]-curY,4.2)
    wheels_y.run_for_degrees(dist, -30)
    curY += beaker2[1]-curY
    print(curX, curY)
    time.sleep(6)
    #time.sleep(2)
    #arms.moveDown()
    #time.sleep(2)
    #arms.moveUp()
    #time.sleep(2)
    

    dist = dist2deg(beaker3[0]-curX,1.3)
    wheels_x.run_for_degrees(dist, -30)
    dist = dist2deg(beaker3[1]-curY,4.2)
    wheels_y.run_for_degrees(dist, 30)
    curX += beaker3[0]-curX
    curY += beaker3[1]-curY
    print(curX, curY)
    time.sleep(6)
    #time.sleep(2)
    #arms.moveDown()
    #time.sleep(2)
    #arms.moveUp()
    #time.sleep(2)
    """

    #arms.release()
    


    """
    
    time.sleep(2)
    arms.moveDown()
    time.sleep(2)
    arms.grip()
    time.sleep(2)
    arms.moveUp()
    time.sleep(2)
    base.moveTo(-1400)    #2200 for the first lot
    time.sleep(3)
    arms.moveDown()
    time.sleep(2)
    liquid.runTest(testData)
    time.sleep(10)
    arms.moveUp()
    time.sleep(2)
    base.moveTo(-2080)
    time.sleep(3)
    arms.moveDown()
    time.sleep(3)
    arms.release()
    time.sleep(3)
    arms.moveUp()
    time.sleep(3)
    base.moveTo(-300)
    time.sleep(4)
    arms.moveDown()
    time.sleep(2)
    arms.grip()
    time.sleep(2)
    arms.moveUp()
    time.sleep(2)
    base.moveTo(-1400)    #2200 for the first lot
    time.sleep(10)
    arms.moveDown()
    time.sleep(2)
    liquid.runTest(testData)
    time.sleep(2)
    arms.moveUp()
    time.sleep(2)
    base.moveTo(-2300)
    time.sleep(2)
    arms.moveDown()
    time.sleep(2)
    arms.release()
    arms.moveUp()
    """
else:
    arms.moveDown()
    time.sleep(3000)
    arms.grip()
    time.sleep(3000)
    arms.moveUp()
    time.sleep(3000)
    base.moveTo(-1300)
    time.sleep(5000)
    arms.moveDown()
    time.sleep(3000)
    arms.release()

    time.sleep(4000)

    ##Second
    arms.moveUp()
    time.sleep(3000)
    base.moveTo(-300)
    time.sleep(3000)
    arms.moveDown()
    time.sleep(3000)
    arms.grip()
    time.sleep(3000)
    arms.moveUp()
    time.sleep(3000)
    base.moveTo(-1460)
    time.sleep(3000)
    arms.moveDown()
    time.sleep(3000)
    arms.release()
    time.sleep(3000)
    arms.moveUp()
    time.sleep(3000)
    base.moveTo(0)
