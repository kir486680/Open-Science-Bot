from Printer import Printer
from Arduino import ArduinoDevice
from Task import Task
from TaskManager import TaskManager
from HelperTask import sleep
import logging

logging.basicConfig(level=logging.INFO)

printer = Printer(port='/dev/tty.usbmodem5CF0515B37301', baudrate=115200)
arduino = ArduinoDevice(port='/dev/tty.usbmodem112201', baudrate=9600)

task_manager = TaskManager()

#task_manager.add_task(Task(printer.home, args=()))

# Example tasks
task_manager.add_task(Task(printer.move_to, args=(None, None, 120, 4000)))
task_manager.add_task(Task(printer.move_to, args=(90.9, None, None, 4000)))
task_manager.add_task(Task(printer.move_to, args=(None, 85, None, 4000)))
task_manager.add_task(Task(printer.move_to, args=(None, None, 47, 4000)))

# #gripper
task_manager.add_task(Task(sleep, args=(1,)))
task_manager.add_task(Task(arduino.grip, args=(1,)))
task_manager.add_task(Task(sleep, args=(1,)))
task_manager.add_task(Task(arduino.grip, args=(2,)))
task_manager.add_task(Task(sleep, args=(1,)))

task_manager.add_task(Task(printer.move_to, args=(None, None, 120, 4000)))
task_manager.add_task(Task(printer.move_to, args=(91.6, None, None, 4000)))
task_manager.add_task(Task(printer.move_to, args=(None, 157.2, None, 4000)))
task_manager.add_task(Task(printer.move_to, args=(None, None, 46.8, 4000)))

#pumpA
task_manager.add_task(Task(sleep, args=(1,)))
task_manager.add_task(Task(arduino.pumpA, args=(25,)))
task_manager.add_task(Task(sleep, args=(3,)))

# # back to the start
# task_manager.add_task(Task(printer.move_to, args=(None, None, 120, 4000)))
# task_manager.add_task(Task(printer.move_to, args=(90.9, None, None, 4000)))
# task_manager.add_task(Task(printer.move_to, args=(None, 85, None, 4000)))
# task_manager.add_task(Task(printer.move_to, args=(None, None, 47, 4000)))

# # gripper
task_manager.add_task(Task(sleep, args=(1,)))
task_manager.add_task(Task(arduino.ungrip, args=(1,)))
task_manager.add_task(Task(sleep, args=(1,)))
task_manager.add_task(Task(arduino.ungrip, args=(2,)))
task_manager.add_task(Task(sleep, args=(1,)))


# # #retract the head
task_manager.add_task(Task(printer.move_to, args=(None, None, 120, 4000)))

# task_manager.add_task(Task(sleep, args=(1,)))
# task_manager.add_task(Task(arduino.pumpB, args=(20,)))
# task_manager.add_task(Task(sleep, args=(1,)))


logging.info("Running tasks")
task_manager.run()
