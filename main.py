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
        self.arm = hub.port.F.motor #the highest it goes is  -120
        self.gripperPos = 0
        self.armPos = 0
        
    def setDefault(self):
        #while not self.arm.was_stalled():
            #self.arm.start(50)
        self.arm.set_degrees_counted(0)
        self.updateCurrentPosition()
    def moveDown(self): # the desired delta is 350
        #self.arm.run_to_position(180, 'counterclockwise', 30) #-400 acceptable
        self.arm.run_for_degrees(340, speed=-40)
        #self.updateCurrentPosition() 
    def moveLower(self): # the desired delta is 350
        #self.arm.run_to_position(180, 'counterclockwise', 30) #-400 acceptable
        self.arm.run_for_degrees(350, speed=-30)
        #self.updateCurrentPosition() 
    def moveUp(self):
      
        #self.arm.run_to_degrees_counted(45,30) 
        self.arm.run_for_degrees(-340, speed=40)
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
    def fromBeaker(self):
        #self.gripper.run_to_position(205,speed=50)
        self.arm.run_for_degrees(-340, speed=40)
        
    def intoBeaker(self):
        #self.gripper.run_to_position(205,speed=50)
        self.arm.run_for_degrees(340, speed=-40)
       
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
    def load_labwear(self, name, locationStart=(0,0), numLots = 3, lotSize = 3.4, taken = [0,0,0],size = 0):
    #fix this the following way https://stackoverflow.com/questions/5079609/methods-with-the-same-name-in-one-class-in-python
        if name == 'MetalHolder':
            metalHolder = self.MetalHolder(locationStart, numLots, taken = taken, lotSize = lotSize) # generate an empty array of 0 be default
            self.peripherals.append(metalHolder)
        if name == 'Beaker':
            beaker = self.Beaker(size, locationStart)
            self.peripherals.append(beaker)

    def encoder(self):

        for i in range(len(self.peripherals)):
            self.peripherals[i].executeLogic()

    class Beaker():
        sizeOptions = [7.3, 7.8] #comes in as [height, radius]
        def __init__(self, size=0, location= (0,0)):
            self.size = self.sizeOptions[size]
            self.start = location
           
        def changeSize(self,size):
            self.size = self.sizeOptions[size]

        def performLogic(self):
            pass

    class MetalHolder():

        
        def __init__(self, locationStart, numLots, taken, lotSize = 3.4):
            
            self.start = locationStart
            self.numLots = numLots
            self.lotSize = lotSize
            self.coordinates = []
            self.taken = taken # array of taken spots of the holder
            self.orientationY = True
            self.generateLocation() # array of x and y coordiates of the spots in the holder
            print(self.status())
        def updateLot(self, idx, status=1):
            self.taken[idx] = status
            #prints out coordinates of the lots with their corresponding statuses
        def status(self):
            for cord,status in zip([[x,y] for x,y in self.coordinates], self.taken):
                print("The point with coordinates x: " + str(cord[0])+ " y: " + str(cord[1]) + " has status " + str(status))
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
        #generates locations of all available
        def generateLocation(self):            
            x, y = self.start
            self.coordinates.append([x,y])
            for i in range(self.numLots-1):
                if self.orientationY: 
                    y += self.lotSize
                    print(self.lotSize)
                else:
                    x += self.lotSize
                self.coordinates.append([x,y])
        def performLogic(self):
            pass
          
        

            

#liquid = LiquidHandler('COM6',9600)

#testData = []
#testData.append("<2,30,1>")
#testData.append("<1,30,1>")
#liquid.runTest(testData)
#liquid.ser.close()

arms = Arm()
base = Base()
board = Board(arms, base)
board.load_labwear('MetalHolder', taken = [1,1,0])
board.load_labwear('Beaker', size = 0, locationStart = (0,7.5))
board.load_labwear('Beaker', size = 0, locationStart = (7.5,7.5))
board.load_labwear('Beaker', size = 1, locationStart = (7.5,15))
board.load_labwear('MetalHolder', locationStart = (7.5,0))
#print(board.peripherals[0].coordinates)
#board.performExperiment("fdf")

#board.encoder()
#arms.setDefault()

debug = True
def dist2deg(desiredDistance, diameter):
    distancePerDegree = np.pi * diameter / 360
    return desiredDistance/distancePerDegree

def dist2deg2(desiredDistance):
    return desiredDistance/0.02666667



if debug ==True:
    wheels_x = hub.port.A.motor
    wheels_y = hub.port.B.motor
    metalSamples = [[0.0,0.0],[3,0]]
    
    beaker1 = (0,5)
    beaker2 = (7.8,5)
    beaker3 = (15.6,5)
    metalDeposit = (15.6,0)
    curX = 0
    curY = 0

    arms.release()

    
    def rotateY(currentY, targetY, diam):
        dist = dist2deg(math.dist([targetY], [currentY]),diam)
        if  targetY-currentY< 0:
            
            wheels_y.run_for_degrees(-dist, -15) 
        else:
            wheels_y.run_for_degrees(dist, 15) 
        currentY += targetY-currentY
        print(currentY)
        return currentY
    def rotateX(currentX, targetX, diam):
        dist = dist2deg(math.dist([targetX], [currentX]),diam)
        if  targetX-currentX < 0:
            wheels_x.run_for_degrees(dist, 40) 
        else:
            wheels_x.run_for_degrees(-dist, -40) 
        currentX += targetX-currentX 
        print(currentX)
        return currentX
    for metalX, metalY in metalSamples:
        print("Starting Itteration")
        curX = rotateX(curX, metalX,1.3)
        curY = rotateY(curY, metalY, 4.2)
        time.sleep(5)
        print("The current is: ", curX, curY)
        arms.moveDown()
        time.sleep(2)
        arms.grip()
        time.sleep(2)
        arms.moveUp()
        time.sleep(2)

        curX = rotateX(curX, beaker1[0],1.3)
        curY = rotateY(curY, beaker1[1], 4.2)
        time.sleep(5)
        print("The current is: ", curX, curY)
        arms.intoBeaker()
        time.sleep(2)
        arms.fromBeaker()
        time.sleep(2)
        

        curX = rotateX(curX, beaker2[0],1.3)
        curY = rotateY(curY, beaker2[1], 4.2)
        time.sleep(5)
        print("The current is: ", curX, curY)
        arms.intoBeaker()
        time.sleep(2)
        arms.fromBeaker()
        time.sleep(2)
        

        curX = rotateX(curX, beaker3[0],1.3)
        curY = rotateY(curY, beaker3[1], 4.2)
        time.sleep(5)
        print("The current is: ", curX, curY)
        arms.intoBeaker()
        time.sleep(2)
        arms.fromBeaker()
        time.sleep(2) 
   
        curX = rotateX(curX, metalDeposit[0],1.3)
        curY = rotateY(curY, metalDeposit[1], 4.2)
        time.sleep(5)
        print("The current is: ", curX, curY)
        arms.intoBeaker()
        time.sleep(2)
        arms.release()
        time.sleep(2) 
        arms.fromBeaker()
        time.sleep(2)


else:
    arms.moveDown()
    time.sleep(2)
    arms.grip()
    time.sleep(2)
    arms.moveUp()
    time.sleep(2)
    arms.release()