from Printer import Printer
from Arduino import ArduinoDevice
from Task import Task
from TaskManager import TaskManager
from HelperTask import sleep
import logging
from Device import DeviceFactory, DeviceType

logging.basicConfig(level=logging.INFO)

from pathlib import Path
from typing import Dict
from RobotSequences import RobotSequences



def main():
    DeviceFactory.register_device(DeviceType.PRINTER, Printer)
    DeviceFactory.register_device(DeviceType.ARDUINO, ArduinoDevice)


    DeviceFactory.load_config('devices.json')

    printer = DeviceFactory.create_device(DeviceType.PRINTER)
    arduino = DeviceFactory.create_device(DeviceType.ARDUINO)

    task_manager = TaskManager()

    robot_sequences = RobotSequences(task_manager, printer, arduino)

    robot_sequences.move_to_start()
    robot_sequences.grip_electrodes()
    robot_sequences.move_to_bath()
    robot_sequences.pump_A()
    robot_sequences.ungrip_both_electrodes()
    robot_sequences.retract_head()



if __name__ == "__main__":
    main()