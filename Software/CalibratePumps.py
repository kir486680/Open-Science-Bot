import time
import logging
import json
import numpy as np
from sklearn.linear_model import LinearRegression
from Arduino import ArduinoDevice
from Task import Task
from HelperTask import sleep

logging.basicConfig(level=logging.INFO)

class PumpCalibrator:
    def __init__(self, arduino_port='/dev/tty.usbmodem112401', baudrate=9600):
        self.arduino = ArduinoDevice(port=arduino_port, baudrate=baudrate)
        self.pump_names = ['B']
        self.directions = ['forward', 'backward']
        self.calibration_results = {}
    
    def run_calibration(self, time_values=None):
        """Run the full calibration procedure for both pumps in both directions"""
        if time_values is None:
            # Default test durations in seconds (5, 10, 15, 20 seconds)
            time_values = [7, 10, 13, 16]
        
        print("\n===== PUMP CALIBRATION PROCEDURE =====")
        print("This procedure will help calibrate the relationship between pump time and volume.")
        print("You'll need a graduated cylinder or measuring container to measure volumes.")
        print("Follow the prompts and enter the volume dispensed after each test.")
        input("Press Enter to begin the calibration...")
        
        for pump in self.pump_names:
            for direction in self.directions:
                print(f"\n== CALIBRATING PUMP {pump} in {direction.upper()} DIRECTION ==")
                
                # Collect measurements
                times = []
                volumes = []
                
                for test_time in time_values:
                    # Run the pump
                    print(f"\nRunning pump {pump} in {direction} direction for {test_time} seconds...")
                    self._run_pump(pump, test_time, direction)
                    
                    # Ask user to measure and enter volume
                    volume = self._get_volume_from_user()
                    if volume is None:  # User wants to skip this test point
                        continue
                    
                    times.append(test_time)
                    volumes.append(volume)
                    
                    # Ask if user wants to continue
                    if not self._continue_calibration():
                        break
                
                if len(times) >= 2:  # Need at least 2 points for linear regression
                    # Calculate calibration parameters
                    params = self._calculate_calibration(times, volumes)
                    self.calibration_results[f"pump{pump}_{direction}"] = params
                    print(f"\nCalibration for Pump {pump} ({direction}): time = ({params['slope']:.4f} * volume_mL + {params['intercept']:.4f})")
                else:
                    print(f"\nNot enough data points for Pump {pump} ({direction}) calibration.")
        
        self._save_calibration()
        print("\nCalibration complete! Results saved to calibration.json")
    
    def _run_pump(self, pump, seconds, direction):
        """Run the specified pump for the given duration and direction"""
        if pump == 'A':
            self.arduino.pumpA(seconds, direction)
        else:
            self.arduino.pumpB(seconds, direction)
        
        # Give a moment for the pump to fully stop
        sleep(1)
    
    def _get_volume_from_user(self):
        """Ask user to measure and enter the dispensed volume"""
        while True:
            try:
                value = input("\nMeasure the dispensed volume and enter the value in mL (or 's' to skip this test): ")
                if value.lower() == 's':
                    return None
                return float(value)
            except ValueError:
                print("Please enter a valid number or 's' to skip.")
    
    def _continue_calibration(self):
        """Ask if user wants to continue with next test"""
        response = input("\nReady for next test? (y/n): ")
        return response.lower() != 'n'
    
    def _calculate_calibration(self, times, volumes):
        """Calculate linear regression parameters for calibration"""
        # Convert to numpy arrays and reshape for sklearn
        times_array = np.array(times).reshape(-1, 1)
        volumes_array = np.array(volumes)
        
        # Fit linear model: time = m * volume + b
        # This will later let us calculate: time_needed = m * desired_volume + b
        model = LinearRegression()
        model.fit(volumes_array.reshape(-1, 1), times_array)
        
        # Extract and return parameters
        slope = model.coef_[0][0]
        intercept = model.intercept_[0]
        
        # Calculate R² to assess fit quality
        r_squared = model.score(volumes_array.reshape(-1, 1), times_array)
        
        return {
            'slope': slope,
            'intercept': intercept,
            'r_squared': r_squared,
            'data_points': {'times': times, 'volumes': volumes}
        }
    
    def _save_calibration(self):
        """Save calibration results to a JSON file"""
        with open('calibration.json', 'w') as f:
            json.dump(self.calibration_results, f, indent=2)


def main():
    print("=== Pump Calibration Tool ===")
    
    # Ask for Arduino port
    default_arduino_port = '/dev/tty.usbmodem112401'  

    # Create calibrator
    calibrator = PumpCalibrator(arduino_port=default_arduino_port)
    
    # Ask for custom time values or use defaults
    use_custom = input("Use custom test durations? (y/n, default: n): ").lower() == 'y'
    time_values = None
    
    if use_custom:
        try:
            time_input = input("Enter 3-5 time values in seconds, separated by spaces (e.g. '5 10 15 20'): ")
            time_values = [float(t) for t in time_input.split()]
            if not (3 <= len(time_values) <= 5):
                print("Number of values outside range (3-5). Using default values.")
                time_values = None
        except ValueError:
            print("Invalid input. Using default values.")
            time_values = None
    
    # Run calibration
    calibrator.run_calibration(time_values)


if __name__ == "__main__":
    main()