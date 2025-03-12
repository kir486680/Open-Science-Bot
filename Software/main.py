from Printer import Printer
from Arduino import ArduinoDevice
from TaskManager import TaskManager
import logging
from Device import DeviceFactory, DeviceType
from RobotSequences import RobotSequences

logging.basicConfig(level=logging.INFO)

def main():
    DeviceFactory.register_device(DeviceType.PRINTER, Printer)
    DeviceFactory.register_device(DeviceType.ARDUINO, ArduinoDevice)


    DeviceFactory.load_config('devices.json')

    printer = DeviceFactory.create_device(DeviceType.PRINTER)
    arduino = DeviceFactory.create_device(DeviceType.ARDUINO)

    task_manager = TaskManager()

    robot_sequences = RobotSequences(task_manager, printer, arduino)

    #robot_sequences.move_to_start()
    robot_sequences.grip_electrodes()
    #robot_sequences.move_to_bath()
    #robot_sequences.pump_A()
    robot_sequences.ungrip_both_electrodes()
    #robot_sequences.retract_head()



if __name__ == "__main__":
    main()