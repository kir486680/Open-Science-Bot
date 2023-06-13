"""
Utility classes to serve as mock imports for running on non-raspberry pi machines.

"""
class MockGPIO:
    BOARD = "BOARD"
    OUT = "OUT"
    IN = "IN"
    HIGH = "HIGH"
    LOW = "LOW"
    BCM = 0

    def setmode(self, mode):
        print(f"Setting mode {mode}")

    def setup(self, pin, mode):
        print(f"Setting up pin {pin} with mode {mode}")

    def output(self, pin, state):
        print(f"Setting pin {pin} state to {state}")

    def cleanup(self):
        print("Cleaning up")

    def PWM(self, pin, pwm):
        print (f"PWM of {pwm} to pin {pin}.")

    # Add more methods and constants as needed based on what you use from RPi.GPIO.


class MockCamera:
    def __init__(self):
        print("Initialising camera mock")
    
    def start_preview(self):
        print("Starting preview mock")

    def stop_preview(self):
        print("Stopping preview mock")

    def capture(self, stream, format):
        print (f"Capturing raspi camera in {format} file format")
        pass



    # Add more methods as needed based on what you use from picamera.