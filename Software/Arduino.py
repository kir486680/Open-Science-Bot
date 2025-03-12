import serial
import json
import logging
import time

class ArduinoDevice:
    def __init__(self, port : str, baudrate : int):
        self.serial = serial.Serial(port, baudrate)
        time.sleep(2)
    
    def send_command(self, command_dict : dict):
        """
        Sends a command to the Arduino and waits for the response
        """
        command_str = json.dumps(command_dict)
        logging.info(f"Sending command: {command_str}")
        
        # Flush buffers
        self.serial.flushInput()
        self.serial.flushOutput()
        
        self.serial.write(f"{command_str}\n".encode())
        logging.info(f"Command sent: {f"{command_str}\n".encode()}")
        
        try:
            response = self.serial.readline().decode().strip()
            logging.info(f"Raw response: {response}")
            if not response:
                logging.error("No response received from Arduino.")
                return None
            response_json = json.loads(response)
            logging.info(f"Deserialized response: {response_json}")
            return response_json
        except json.JSONDecodeError as e:
            logging.error(f"Failed to decode JSON response: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            raise
    
    def dispense(self, volume : float):
        """
        Dispenses a given volume of liquid
        """
        command = {"device": "pump", "action": "dispense", "parameters": {"volume": volume}}
        return self.send_command(command)
    
    def move_motor(self, position : float):
        """
        Moves the motor to a given position
        """
        command = {"device": "motor", "action": "move", "parameters": {"position": position}}
        return self.send_command(command)
    
    def grip(self, gripper_number : int):
        """
        Grips the gripper
        """
        command = {"device": "gripper", "action": "grip", "parameters": {"gripper_number": gripper_number}}
        response = self.send_command(command)
        if response.get("status") != "ok":
            raise Exception("Failed to execute grip command")
        return response
    
    def ungrip(self, gripper_number : int):
        """
        Ungrips the gripper
        """
        command = {"device": "gripper", "action": "ungrip", "parameters": {"gripper_number": gripper_number}}
        response = self.send_command(command)
        if response.get("status") != "ok":
            raise Exception("Failed to execute ungrip command")
        return response
    
    def pumpA(self, seconds : float, direction : str = "forward"):
        """
        Pumps liquid in the A direction
        """
        command = {"device": "pumpA", "action": "run", "parameters": {"duration": seconds, "direction": direction}}
        return self.send_command(command)

    def pumpB(self, seconds : float, direction : str = "forward"):
        """
        Pumps liquid in the B direction
        """
        command = {"device": "pumpB", "action": "run", "parameters": {"duration": seconds, "direction": direction}}
        return self.send_command(command)