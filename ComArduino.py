# 19 July 2014

# in case any of this upsets Python purists it has been converted from an equivalent JRuby program

# this is designed to work with ... ArduinoPC2.ino ...

# the purpose of this program and the associated Arduino program is to demonstrate a system for sending 
#   and receiving data between a PC and an Arduino.

# The key functions are:
#    sendToArduino(str) which sends the given string to the Arduino. The string may 
#                       contain characters with any of the values 0 to 255
#
#    recvFromArduino()  which returns an array. 
#                         The first element contains the number of bytes that the Arduino said it included in
#                             message. This can be used to check that the full message was received.
#                         The second element contains the message as a string


# the overall process followed by the demo program is as follows
#   open the serial connection to the Arduino - which causes the Arduino to reset
#   wait for a message from the Arduino to give it time to reset
#   loop through a series of test messages
#      send a message and display it on the PC screen
#      wait for a reply and display it on the PC

# to facilitate debugging the Arduino code this program interprets any message from the Arduino
#    with the message length set to 0 as a debug message which is displayed on the PC screen

# the message to be sent to the Arduino starts with < and ends with >
#    the message content comprises a string, an integer and a float
#    the numbers are sent as their ascii equivalents
#    for example <LED1,200,0.2>
#    this means set the flash interval for LED1 to 200 millisecs
#      and move the servo to 20% of its range

# receiving a message from the Arduino involves
#    waiting until the startMarker is detected
#    saving all subsequent bytes until the end marker is detected

# NOTES
#       this program does not include any timeouts to deal with delays in communication
#
#       for simplicity the program does NOT search for the comm port - the user must modify the
#         code to include the correct reference.
#         search for the lines 
#               serPort = "/dev/ttyS80"
#               baudRate = 9600
#               ser = serial.Serial(serPort, baudRate)
#


#=====================================

#  Function Definitions

#=====================================

import serial
import time

class LiquidHandler():

  def __init__(self, serPort, baudRate):
    # NOTE the user must ensure that the serial port and baudrate are correct
    self.serPort = serPort
    self.baudRate = baudRate
    self.ser = serial.Serial(serPort, baudRate)
    print("Serial port " + self.serPort + " opened  Baudrate " + str(self.baudRate))


    self.startMarker = 60
    self.endMarker = 62
    self.waitForArduino()
  def sendToArduino(self,sendStr):
    self.ser.write(sendStr.encode('utf-8'))


  #======================================

  def recvFromArduino(self):
    global startMarker, endMarker
    
    ck = ""
    x = "z" # any value that is not an end- or startMarker
    byteCount = -1 # to allow for the fact that the last increment will be one too many
    
    # wait for the start character
    while  ord(x) != self.startMarker: 
      x = self.ser.read()
    
    # save data until the end marker is found
    while ord(x) != self.endMarker:
      if ord(x) != self.startMarker:
        ck = ck + x.decode("utf-8") 
        byteCount += 1
      x = self.ser.read()
    
    return(ck)


  #============================

  def waitForArduino(self):

    # wait until the Arduino sends 'Arduino Ready' - allows time for Arduino reset
    # it also ensures that any bytes left over from a previous message are discarded
    
      global startMarker, endMarker
      
      msg = ""
      while msg.find("Arduino is ready") == -1:

        while self.ser.inWaiting() == 0:
          pass
          
        msg = self.recvFromArduino()

        print(msg)
      
      
#======================================

  def runTest(self,td):
    numLoops = len(td)
    waitingForReply = False

    n = 0
    while n < numLoops:

      teststr = td[n]

      if waitingForReply == False:
        self.sendToArduino(teststr)
        print("Sent from PC -- LOOP NUM " + str(n) + " TEST STR " + teststr)
        waitingForReply = True

      if waitingForReply == True:

        while self.ser.inWaiting() == 0:
          pass
          
        dataRecvd = self.recvFromArduino()
        print("Reply Received  " + dataRecvd)
        n += 1
        waitingForReply = False

        print("===========")

      time.sleep(5)



