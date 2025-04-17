from Task import Task
from TaskManager import TaskManager
from HelperTask import sleep
from Printer import Printer
from Arduino import ArduinoDevice
from Potentiostat import PotentiostatDevice


class RobotSequences:
    """Class to organize and manage robot operation sequences"""
    def __init__(self, task_manager: TaskManager, printer: Printer, arduino: ArduinoDevice, potentiostat: PotentiostatDevice):
        self.task_manager = task_manager
        self.printer = printer
        self.arduino = arduino
        self.potentiostat = potentiostat
    
    def move_to_start(self):
        """
        Moves the robot to the start position
        """
        with self.task_manager.execute_sequence("move_to_start"):
            self.task_manager.add_task(Task(
                self.printer.move_to,
                args=(None, None, 120, 4000),
                description="Move Z to safe height"
            ))
            self.task_manager.add_task(Task(
                self.printer.move_to,
                args=(90.9, None, None, 4000),
                description="Move X to start position"
            ))
            self.task_manager.add_task(Task(
                self.printer.move_to,
                args=(None, 85, None, 4000),
                description="Move Y to start position"
            ))
            self.task_manager.add_task(Task(
                self.printer.move_to,
                args=(None, None, 47, 4000),
                description="Lower Z to working height"
            ))

    def grip_electrodes(self):
        """
        Grips the electrodes
        """
        with self.task_manager.execute_sequence("grip_both_electrodes"):
            self.task_manager.add_task(Task(sleep, args=(1,), description="Pre-grip delay"))
            self.task_manager.add_task(Task(
                self.arduino.grip,
                args=(1,),
                description="Grip first electrode"
            ))
            self.task_manager.add_task(Task(sleep, args=(1,), description="Inter-grip delay"))
            self.task_manager.add_task(Task(
                self.arduino.grip,
                args=(2,),
                description="Grip second electrode"
            ))
            self.task_manager.add_task(Task(sleep, args=(1,), description="Post-grip delay"))
    
    def ungrip_both_electrodes(self):
        """
        Ungrips the electrodes
        """
        with self.task_manager.execute_sequence("ungrip_both_electrodes"):
            self.task_manager.add_task(Task(sleep, args=(1,)))
            self.task_manager.add_task(Task(self.arduino.ungrip, args=(1,)))
            self.task_manager.add_task(Task(sleep, args=(1,)))
            self.task_manager.add_task(Task(self.arduino.ungrip, args=(2,)))
            self.task_manager.add_task(Task(sleep, args=(1,)))

    def move_to_bath(self):
        """
        Moves the robot to the bath position
        """
        with self.task_manager.execute_sequence("move_to_bath"):
            self.task_manager.add_task(Task(
                self.printer.move_to,
                args=(None, None, 120, 4000),
                description="Move to bath"
            ))
            self.task_manager.add_task(Task(
                self.printer.move_to,
                args=(91.6, None, None, 4000),
                description="Move X to bath position"
            ))
            self.task_manager.add_task(Task(
                self.printer.move_to,
                args=(None, 157.2, None, 4000),
                description="Move Y to bath position"
            ))
            self.task_manager.add_task(Task(
                self.printer.move_to,
                args=(None, None, 46.8, 4000),
                description="Move Z to bath position"
            ))

    def pump_A(self):
        """
        Pumps liquid in the A direction
        """
        with self.task_manager.execute_sequence("pump_A"):
            self.task_manager.add_task(Task(sleep, args=(1,)))
            self.task_manager.add_task(Task(self.arduino.pumpA, args=(25,)))
            self.task_manager.add_task(Task(sleep, args=(3,)))

    def retract_head(self):
        """
        Retracts the head
        """
        with self.task_manager.execute_sequence("retract_head"):
            self.task_manager.add_task(Task(
                self.printer.move_to,
                args=(None, None, 120, 4000),
                description="Retract head"
            ))

    # Updated potentiostat methods using the new interface
    def setup_pstat_test(self):
        """Prepare potentiostat for measurement"""
        if not self.potentiostat:
            raise Exception("Potentiostat not initialized")
            
        with self.task_manager.execute_sequence("setup_pstat"):
            self.task_manager.add_task(Task(
                self.potentiostat.connect_electrodes,
                args=(True,),
                description="Connect WE and CE"
            ))
    
    def measure_ocp(self, sample_name, duration_s=300, sample_rate_hz=1, save_data=True):
        """Run Open Circuit Potential measurement"""
        if not self.potentiostat:
            raise Exception("Potentiostat not initialized")
            
        results = []
        
        with self.task_manager.execute_sequence("measure_ocp"):
            def _measure_ocp_task():
                data = self.potentiostat.measure_ocp(duration_s, sample_rate_hz)
                results.append(data)
                
                if save_data and sample_name:
                    self.potentiostat.save_data(
                        data, 
                        f"{sample_name}_ocp.csv", 
                        "Time(s),Potential(V)"
                    )
                
                return data
            
            self.task_manager.add_task(Task(_measure_ocp_task, description="Measuring OCP"))
        
        return results[0] if results else None
    
    def perform_lpr(self, sample_name, start_offset_V=-0.02, end_offset_V=0.025, 
                  scan_rate_V_s=0.01, save_data=True):
        """Run Linear Polarization Resistance measurement"""
        if not self.potentiostat:
            raise Exception("Potentiostat not initialized")
            
        results = []
        
        with self.task_manager.execute_sequence("perform_lpr"):
            def _perform_lpr_task():
                data = self.potentiostat.perform_lpr(
                    start_offset_V, 
                    end_offset_V, 
                    scan_rate_V_s
                )
                results.append(data)
                
                if save_data and sample_name:
                    self.potentiostat.save_data(
                        data, 
                        f"{sample_name}_lpr.csv", 
                        "Potential(V),Current(A)"
                    )
                
                return data
            
            self.task_manager.add_task(Task(_perform_lpr_task, description="Performing LPR"))
        
        return results[0] if results else None
    
    def perform_cv(self, sample_name, amplitude_V=0.5, scan_rate_V_s=0.05, save_data=True):
        """Run Cyclic Voltammetry measurement"""
        if not self.potentiostat:
            raise Exception("Potentiostat not initialized")
            
        results = []
        
        with self.task_manager.execute_sequence("perform_cv"):
            def _perform_cv_task():
                data = self.potentiostat.perform_cv(amplitude_V, scan_rate_V_s)
                results.append(data)
                
                if save_data and sample_name:
                    self.potentiostat.save_data(
                        data, 
                        f"{sample_name}_cv.csv", 
                        "Potential(V),Current(A)"
                    )
                
                return data
            
            self.task_manager.add_task(Task(_perform_cv_task, description="Performing CV"))
        
        return results[0] if results else None
    
    def run_electrochemical_sequence(self, sample_name, save_data=True):
        """Run a complete electrochemical test sequence"""
        if not self.potentiostat:
            raise Exception("Potentiostat not initialized")
            
        with self.task_manager.execute_sequence("electrochemical_sequence"):
            print(f"Starting full electrochemical sequence for {sample_name}")
            
            # Setup potentiostat
            self.setup_pstat_test()
            
            # 1. Initial OCP
            ocp_data = self.measure_ocp(sample_name + "_initial", duration_s=300, save_data=save_data)
            
            # 2. LPR
            lpr_data = self.perform_lpr(sample_name, save_data=save_data)
            
            # Reset potentiostat
            self.task_manager.add_task(Task(self.potentiostat.reset, description="Reset potentiostat"))
            
            # 3. Short OCP
            ocp_data_2 = self.measure_ocp(sample_name + "_second", duration_s=100, save_data=save_data)
            
            # 4. CV
            cv_data = self.perform_cv(sample_name, save_data=save_data)
            
            return {
                'initial_ocp': ocp_data,
                'lpr': lpr_data,
                'second_ocp': ocp_data_2,
                'cv': cv_data
            }


