"""
Utility classes to serve as mock imports for running on non-raspberry pi machines.

"""
import numpy as np

class MockGPIO:
    BOARD = "BOARD"
    OUT = "OUT"
    IN = "IN"
    HIGH = "HIGH"
    LOW = "LOW"
    BCM = 0

    

    def setmode(self):
        print(f"Setting mode")

    def setup(self, pin):
        print(f"Setting up pin {pin} with mode")

    def output(self, pin, state):
        print(f"Setting pin {pin} state to {state}")

    def cleanup():
        print("Cleaning up")

    class PWM:
        def __init__(self, pin, pwm):
            print (f"PWM of {pwm} to pin {pin}.")

        def stop(self):
            print("stopped")

        def ChangeDutyCycle(self, num):
            print(f"changed duty cycle to {num}")

        def start(self, num):
            print(f"started at {num}")

    # Add more methods and constants as needed based on what you use from RPi.GPIO.

class MockCamera:
    
    def __init__(self):
        print("Initialising camera mock")
        self.camera_type = ""
        
    class PiCamera:
        def __init__(self):
            pass
        
        def capture(self, stream, format):
            print (f"Capturing raspi camera in {format} file format")
            #generate a jpeg 
    
    def start_preview(self):
        print("Starting preview mock")

    def stop_preview(self):
        print("Stopping preview mock")

   



    # Add more methods as needed based on what you use from picamera.