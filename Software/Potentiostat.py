import pstat.Potentiostat as ps
from pstat.Potentiostat.potentiostat import Resistors, DAC, ADC
import numpy as np
import time
import logging
import os
from datetime import datetime

class PotentiostatDevice:
    """Interface for the potentiostat device"""
    
    def __init__(self, port: str):
        """Initialize potentiostat connection"""
        self.pstat = ps.Potentiostat(port)
        self.pstat.connect()
        
        # Initialize with default gain
        self.pstat.write_gain(Resistors.R_10K)
        
        # Initialize DAC
        self.pstat.write_dac(channels=[DAC.CE_IN, DAC.A_REF, DAC.V_AN], 
                           voltages=[0, -5, 0])
        
        logging.info(f"Potentiostat connected on port {port}")
    
    def connect_electrodes(self, connect: bool = True) -> None:
        """Connect or disconnect working and counter electrodes"""
        self.pstat.write_switch(connect)
        logging.info(f"Electrodes {'connected' if connect else 'disconnected'}")
        time.sleep(1)  # Allow system to stabilize
    
    def set_gain(self, resistor: Resistors = Resistors.R_10K) -> None:
        """Set the gain resistor"""
        self.pstat.write_gain(resistor)
        logging.info(f"Gain set to {resistor}")
    
    def set_potential(self, potential_V: float) -> None:
        """Set the working electrode potential"""
        self.pstat.write_potential(potential_V)
        logging.info(f"Potential set to {potential_V}V")
    
    def read_ocp(self) -> float:
        """Read the open circuit potential"""
        ocp = self.pstat.read_ocp()
        logging.info(f"OCP read: {ocp}V")
        return ocp
    
    def read_potential_current(self) -> tuple:
        """Read the current potential and current"""
        potential, current = self.pstat.read_potential_current()
        logging.info(f"Read: {potential}V, {current*1e6}µA")
        return potential, current
    
    def measure_ocp(self, duration_s=300, sample_rate_hz=1) -> np.ndarray:
        """
        Measure Open Circuit Potential over time
        Returns: numpy array of [time, potential] values
        """
        logging.info(f"Starting OCP measurement for {duration_s}s at {sample_rate_hz}Hz")
        samples = int(duration_s * sample_rate_hz)
        data = np.zeros((samples, 2))
        
        start_time = datetime.now()
        for i in range(samples):
            potential = self.read_ocp()
            
            current_time = (datetime.now() - start_time).total_seconds()
            data[i] = [current_time, potential]
            time.sleep(1/sample_rate_hz)
            
        return data
    
    def perform_lpr(self, start_offset_V=-0.02, end_offset_V=0.025, 
                   scan_rate_V_s=0.01) -> np.ndarray:
        """
        Perform Linear Polarization Resistance measurement
        Returns: numpy array of [potential, current] values
        """
        logging.info("Starting LPR measurement")
        
        # Read OCP as starting point with multiple readings for stability
        ocp_readings = []
        for _ in range(5):
            ocp_readings.append(self.pstat.read_potential()[0])
            time.sleep(0.5)
        ocp = np.mean(ocp_readings)
        logging.info(f"Initial OCP: {ocp:.3f}V")
        
        # Calculate voltage steps
        step_size_V = 0.001  # 1mV steps
        start_V = ocp + start_offset_V
        end_V = ocp + end_offset_V
        voltages = np.arange(start_V, end_V, step_size_V)
        delay_s = step_size_V / scan_rate_V_s
        
        # Prepare data storage
        results = []
        
        # Initial stabilization at start potential
        self.set_potential(start_V)
        time.sleep(5)
        
        # Perform voltage sweep
        for target_V in voltages:
            self.set_potential(target_V)
            time.sleep(delay_s)
            
            # Take multiple readings and average
            potentials = []
            currents = []
            for _ in range(3):
                potential, current = self.read_potential_current()
                potentials.append(potential)
                currents.append(current)
                time.sleep(0.2)
            
            avg_potential = np.mean(potentials)
            avg_current = np.mean(currents)
            results.append([avg_potential, avg_current])
        
        # Reset system
        self.reset()
        
        return np.array(results)
    
    def perform_cv(self, amplitude_V=0.5, scan_rate_V_s=0.05) -> np.ndarray:
        """
        Perform Cyclic Voltammetry
        Returns: numpy array of [potential, current] values
        """
        logging.info("Starting CV measurement")
        
        # Read OCP as starting point
        ocp = self.pstat.read_potential()[0]
        
        # Set up CV parameters and run
        return self.pstat.perform_CV(
            min_V=ocp - amplitude_V,
            max_V=ocp + amplitude_V,
            cycles=1,
            mV_s=scan_rate_V_s * 1000,  # Convert to mV/s
            step_hz=250,
            start_V=ocp,
            last_V=ocp
        )
    
    def reset(self) -> None:
        """Reset the system to default state"""
        self.connect_electrodes(False)
        time.sleep(1)
        self.connect_electrodes(True)
        time.sleep(1)
        self.set_gain()
        self.pstat.write_dac(channels=[DAC.CE_IN, DAC.A_REF, DAC.V_AN], 
                           voltages=[0, -5, 0])
        time.sleep(1)
        logging.info("Potentiostat reset to default state")
    
    def disconnect(self) -> None:
        """Disconnect from the potentiostat"""
        self.connect_electrodes(False)
        self.pstat.disconnect()
        logging.info("Potentiostat disconnected")
    
    def save_data(self, data: np.ndarray, filename: str, headers: str) -> None:
        """Save measurement data to a CSV file"""
        os.makedirs("data", exist_ok=True)
        np.savetxt(f"data/{filename}", data, delimiter=",", header=headers)
        logging.info(f"Data saved to data/{filename}")