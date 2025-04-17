from Printer import Printer
from Arduino import ArduinoDevice
from Potentiostat import PotentiostatDevice
from TaskManager import TaskManager
import logging
from Device import DeviceFactory, DeviceType
from RobotSequences import RobotSequences

logging.basicConfig(level=logging.INFO)

def main():
    DeviceFactory.register_device(DeviceType.PRINTER, Printer)
    DeviceFactory.register_device(DeviceType.ARDUINO, ArduinoDevice)
    DeviceFactory.register_device(DeviceType.POTENTIOSTAT, PotentiostatDevice)

    DeviceFactory.load_config('devices.json')

    printer = DeviceFactory.create_device(DeviceType.PRINTER)
    arduino = DeviceFactory.create_device(DeviceType.ARDUINO)
    potentiostat = DeviceFactory.create_device(DeviceType.POTENTIOSTAT)

    task_manager = TaskManager()

    robot_sequences = RobotSequences(task_manager, printer, arduino, potentiostat)

    # Example sequence
    try:
        robot_sequences.move_to_start()
        robot_sequences.grip_electrodes()
        robot_sequences.move_to_bath()
        
        # Run an electrochemical test
        sample_name = "test_sample"
        robot_sequences.run_electrochemical_sequence(sample_name)
        
        robot_sequences.ungrip_both_electrodes()
        robot_sequences.retract_head()
    finally:
        # Clean up
        if potentiostat:
            potentiostat.disconnect()

if __name__ == "__main__":
    main()