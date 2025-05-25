import numpy as np
from skopt import gp_minimize
from skopt.space import Real
import matplotlib.pyplot as plt
from Device import DeviceFactory, DeviceType
from Arduino import ArduinoDevice
from Potentiostat import PotentiostatDevice
import time
import logging
import csv

logging.basicConfig(level=logging.INFO)

class BayesianOptimizer:
    def __init__(self, arduino_port=None, pstat_port="/dev/ttyACM0"):
        # Initialize Arduino
        DeviceFactory.register_device(DeviceType.ARDUINO, ArduinoDevice)
        self.arduino = DeviceFactory.create_device(DeviceType.ARDUINO)
        
        # Initialize potentiostat using existing PotentiostatDevice class
        self.pstat = PotentiostatDevice(pstat_port)
        
        # Initialize volume tracking
        self.current_volume = 0

    def pump_vinegar(self, volume):
        # Ensure volume is within safe limits
        volume = np.clip(volume, 5.0, 50.0) 
        
        print(f"Current volume: {self.current_volume}mL, Target volume: {volume}mL")
        
        # Calculate how much vinegar to add based on current volume
        volume_to_add = max(0, volume - self.current_volume)
        
        if volume_to_add > 0:
            print(f"Pumping {volume_to_add}mL vinegar")
            time.sleep(1)
            self.arduino.pumpB(volume_to_add, direction="forward", use_calibration=True)
            time.sleep(1)
            self.current_volume = volume
            print(f"New current volume: {self.current_volume}mL")
        elif volume < self.current_volume:
            volume_to_remove = self.current_volume - volume
            print(f"Removing {volume_to_remove}mL")
            time.sleep(1)
            self.arduino.pumpA(volume_to_remove, direction="forward", use_calibration=True)
            time.sleep(1)
            self.current_volume = volume
            print(f"New current volume: {self.current_volume}mL")
        else:
            print(f"No volume change needed, current volume: {self.current_volume}mL")
    
    def measure_ocp(self, duration=10, stabilization_time=60):
        """Measure OCP with stabilization period"""
        print(f"\nStabilization period: {stabilization_time} seconds")
        print("Taking readings every 10 seconds during stabilization...")
        
        # Disconnect electrodes for OCP measurement
        self.pstat.connect_electrodes(False)
        
        # Stabilization readings
        stabilization_readings = []
        start_time = time.time()
        
        while (time.time() - start_time) < stabilization_time:
            current_time = time.time() - start_time
            potential = self.pstat.read_ocp()
            stabilization_readings.append(potential)
            
            print(f"Time: {current_time:.1f}s | Stabilization Potential: {potential:.3f}V")
            
            # Wait for next reading
            remaining_time = stabilization_time - (time.time() - start_time)
            if remaining_time > 10:
                time.sleep(10)
            elif remaining_time > 0:
                time.sleep(remaining_time)
        
        # Main measurement using built-in method
        print(f"\nStarting main OCP measurement for {duration} seconds...")
        data = self.pstat.measure_ocp(
            duration_s=duration,
            sample_rate_hz=1
        )
        
        # Save data to CSV
        filename = f"ocp_measurement_vol_{self.current_volume:.1f}mL.csv"
        self.pstat.save_data(
            data, 
            filename, 
            "Time(s),Potential(V)"
        )
        
        return {
            'potential': data[:, 1],
            'time': data[:, 0],
            'mean_potential': np.mean(data[:, 1])
        }
    
    def run_optimization(self, target_ocp=-0.1, n_calls=15, n_random_starts=4):
        """Run Bayesian optimization to find best volume"""
        # Define objective function
        def objective_function(volume):
            vol = volume[0] if isinstance(volume, list) else volume
            
            print(f"\nBayesian optimization selected volume: {vol:.2f}mL")
            self.pump_vinegar(vol)
            
            ocp_data = self.measure_ocp(duration=10, stabilization_time=200)
            measured_ocp = ocp_data['mean_potential']
            
            # Calculate error
            error = abs(measured_ocp - target_ocp)
            print(f"\nTested volume: {vol:.2f}mL")
            print(f"Measured OCP: {measured_ocp:.3f}V")
            print(f"Error from target: {error:.3f}V")
            print(f"Current system volume: {self.current_volume:.2f}mL")
            
            # Plot the measurement
            plt.figure(figsize=(10, 4))
            plt.plot(ocp_data['time'], ocp_data['potential'])
            plt.xlabel('Time (s)')
            plt.ylabel('Potential (V)')
            plt.title(f'OCP Measurement at {vol:.1f}mL')
            plt.grid(True)
            plt.savefig(f'ocp_measurement_vol_{vol:.1f}mL.png')
            plt.close()
            
            return error
        
        # Define search space
        search_space = [Real(5.0, 50.0, name='volume')]
        
        try:
            # Run optimization
            print("\nStarting Bayesian optimization...")
            print(f"Target OCP: {target_ocp:.3f}V")
            
            result = gp_minimize(
                objective_function,
                search_space,
                n_calls=n_calls,
                n_random_starts=n_random_starts,
                random_state=42,
                verbose=True
            )
            
            # Report results
            best_volume = result.x[0]
            print(f"\nOptimization complete!")
            print(f"Best volume found: {best_volume:.2f} mL")
            print(f"Target OCP: {target_ocp:.3f} V")
            
            # Final verification
            print("\nPerforming final verification measurement...")
            self.pump_vinegar(best_volume)
            final_ocp_data = self.measure_ocp(duration=5, stabilization_time=60)
            final_ocp = final_ocp_data['mean_potential']
            print(f"Final measured OCP: {final_ocp:.3f} V")
            
            # Plot optimization progress
            plt.figure(figsize=(10, 6))
            plt.plot(range(len(result.func_vals)), result.func_vals, 'o-')
            plt.xlabel('Iteration')
            plt.ylabel('|Measured OCP - Target OCP| (V)')
            plt.title('Bayesian Optimization Progress')
            plt.grid(True)
            plt.savefig('optimization_progress.png')
            plt.show()
            
            return result
            
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up and disconnect devices"""
        self.pstat.disconnect()
        print("System disconnected")

def main():
    # Create optimizer with default ports from devices.json
    optimizer = BayesianOptimizer(
        pstat_port="/dev/tty.usbmodem2055349133301"
    )
    
    # Run optimization with default parameters
    optimizer.run_optimization(
        target_ocp=-0.1,
        n_calls=15,
        n_random_starts=4
    )

if __name__ == "__main__":
    main()