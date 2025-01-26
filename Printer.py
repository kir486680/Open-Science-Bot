import serial
import time
import logging

class Printer:
    def __init__(self, port, baudrate):
        self.serial = serial.Serial(port, baudrate)
        time.sleep(2)

    
    def send_command(self, command):
        logging.info(f"Sending command: {command}")
        self.serial.write((command + '\n').encode())
        self.wait_for_ok()

    def wait_for_ok(self):
        while True:
            response = self.serial.readline().decode().strip()
            if response == "ok":
                logging.info("Completed command")
                return  
            elif response:
                logging.info(f"Printer response: {response}")
    def wait_for_completion(self):
        logging.info("Waiting for completion")
        self.send_command("M400")  # Wait for all movements to complete

    def move_to(self, x=None, y=None, z=None, speed=4000):
        """
        Moves the printer to the specified coordinates. If x or y is not provided,
        the current position is maintained.
        
        :param x: X coordinate to move to (optional)
        :param y: Y coordinate to move to (optional)
        :param z: Z coordinate to move to (optional)
        :param speed: Speed of the movement (optional, default is 4000)
        """
        # Construct the G-code command
        command = "G1"
        if x is not None:
            command += f" X{x}"
        if y is not None:
            command += f" Y{y}"
        if z is not None:
            command += f" Z{z}"
        command += f" F{speed}"

        self.send_command(command)
        self.wait_for_completion()  # Wait for the command to complete
        logging.info("Completed move")

    def home(self, axes=""):
        """
        Homes the specified axes. If no axes are specified, all axes are homed.
        :param axes: A string containing the axes to home, e.g., "X", "Y", "Z".
        """
        command = f"G28 {axes}"
        self.send_command(command)
        self.wait_for_completion()  # Wait for the homing command to complete
        logging.info("Completed homing")