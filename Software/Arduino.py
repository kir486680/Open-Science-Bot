import serial
import json
import logging
import time

class ArduinoDevice:
    def __init__(self, port: str, baudrate: int, calibration_params=None):
        self.serial = serial.Serial(port, baudrate)
        time.sleep(2)
        
        # Load calibration parameters
        if calibration_params:
            self.pump_calibration = calibration_params
        else:
            # Load from devices.json as fallback
            try:
                with open('devices.json', 'r') as f:
                    devices_config = json.load(f)
                    self.pump_calibration = devices_config['arduino'].get('pump_calibration', {})
            except (FileNotFoundError, KeyError, json.JSONDecodeError):
                logging.warning("No pump calibration parameters found")
                self.pump_calibration = {}

    def _calculate_pump_time(self, volume_ml: float, pump: str, direction: str = "forward") -> float:
        """
        Calculate the time needed to pump a specific volume based on calibration
        """
        key = f"pump{pump}_{direction}"
        if key in self.pump_calibration:
            params = self.pump_calibration[key]
            seconds = params['slope'] * volume_ml + params['intercept']
            return seconds
        else:
            logging.warning(f"No calibration found for {key}, using direct time value")
            return volume_ml  # Fallback to using volume as time directly

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
    
    def pumpA(self, volume_or_seconds: float, direction: str = "forward", use_calibration: bool = True):
        """
        Pumps liquid using pump A
        Args:
            volume_or_seconds: If use_calibration=True, this is volume in mL. If False, this is time in seconds
            direction: "forward" or "reverse"
            use_calibration: Whether to use calibration to convert volume to time
        """
        if use_calibration:
            seconds = self._calculate_pump_time(volume_or_seconds, 'A', direction)
        else:
            seconds = volume_or_seconds
            
        command = {"device": "pumpA", "action": "run", "parameters": {"duration": seconds, "direction": direction}}
        return self.send_command(command)

    def pumpB(self, volume_or_seconds: float, direction: str = "forward", use_calibration: bool = True):
        """
        Pumps liquid using pump B
        Args:
            volume_or_seconds: If use_calibration=True, this is volume in mL. If False, this is time in seconds
            direction: "forward" or "reverse"
            use_calibration: Whether to use calibration to convert volume to time
        """
        if use_calibration:
            seconds = self._calculate_pump_time(volume_or_seconds, 'B', direction)
        else:
            seconds = volume_or_seconds
            
        command = {"device": "pumpB", "action": "run", "parameters": {"duration": seconds, "direction": direction}}
        return self.send_command(command)