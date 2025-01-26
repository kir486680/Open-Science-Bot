from Printer import Printer
from Arduino import ArduinoDevice
from Task import Task
from TaskManager import TaskManager
from HelperTask import sleep
import logging

logging.basicConfig(level=logging.INFO)

#printer = Printer(port='/dev/tty.usbmodem5CF0515B37301', baudrate=115200)
arduino = ArduinoDevice(port='/dev/tty.usbmodem112401', baudrate=9600)

task_manager = TaskManager()

# # Example tasks
# task_manager.add_task(Task(printer.home, args=()))
# task_manager.add_task(Task(printer.move_to, args=(None, None, 100, 4000)))
# task_manager.add_task(Task(printer.move_to, args=(92, None, None, 4000)))
# task_manager.add_task(Task(printer.move_to, args=(None, 85, None, 4000)))
# task_manager.add_task(Task(printer.move_to, args=(None, None, 45, 4000)))

# #gripper
# task_manager.add_task(Task(sleep, args=(1,)))
# task_manager.add_task(Task(arduino.grip, args=(1,)))
# task_manager.add_task(Task(sleep, args=(2,)))
# task_manager.add_task(Task(arduino.grip, args=(2,)))
# task_manager.add_task(Task(sleep, args=(1,)))


# gripper
# task_manager.add_task(Task(sleep, args=(1,)))
# task_manager.add_task(Task(arduino.ungrip, args=(1,)))
# task_manager.add_task(Task(sleep, args=(1,)))
# task_manager.add_task(Task(arduino.ungrip, args=(2,)))
# task_manager.add_task(Task(sleep, args=(1,)))


# #retract the head
#task_manager.add_task(Task(printer.move_to, args=(None, None, 90, 4000)))

# task_manager.add_task(Task(sleep, args=(1,)))
# task_manager.add_task(Task(arduino.pumpA, args=(16.33, "reverse")))
# task_manager.add_task(Task(sleep, args=(1,)))


#10 s -> 7.5mL
#15s -> 14.5mL
#20s -> 23mL
#11.7s -> 9.5mL
#16.33s -> 17mL

def pumpAFOrwwardCalibration(VolumeML):
    seconds = (VolumeML + 8.578) / 1.566
    return seconds

def pumpBFOrwwardCalibration(VolumeML):
    #19.02948885976409s -> 26mL
    seconds = (VolumeML + 4.776) / 1.513
    print(seconds)
    return seconds

task_manager.add_task(Task(sleep, args=(1,)))
task_manager.add_task(Task(arduino.pumpA, args=(pumpBFOrwwardCalibration(15), "reverse")))
task_manager.add_task(Task(sleep, args=(1,)))

#10s  -> 9.8 mL
#12s -> 13.5 mL
#15s -> 18.2 mL
#17s -> 21.4 mL



logging.info("Running tasks")
task_manager.run()
