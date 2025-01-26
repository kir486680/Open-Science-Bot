from Task import Task
from TaskManager import TaskManager
from HelperTask import sleep
from Printer import Printer
from Arduino import Arduino

class RobotSequences:
    """Class to organize and manage robot operation sequences"""
    def __init__(self, task_manager: TaskManager, printer : Printer, arduino : Arduino):
        self.task_manager = task_manager
        self.printer = printer
        self.arduino = arduino

    def move_to_start(self):
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
        with self.task_manager.execute_sequence("ungrip_both_electrodes"):
            self.task_manager.add_task(Task(sleep, args=(1,)))
            self.task_manager.add_task(Task(self.arduino.ungrip, args=(1,)))
            self.task_manager.add_task(Task(sleep, args=(1,)))
            self.task_manager.add_task(Task(self.arduino.ungrip, args=(2,)))
            self.task_manager.add_task(Task(sleep, args=(1,)))

    def move_to_bath(self):
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
        with self.task_manager.execute_sequence("pump_A"):
            self.task_manager.add_task(Task(sleep, args=(1,)))
            self.task_manager.add_task(Task(self.arduino.pumpA, args=(25,)))
            self.task_manager.add_task(Task(sleep, args=(3,)))

    def retract_head(self):
        with self.task_manager.execute_sequence("retract_head"):
            self.task_manager.add_task(Task(
                self.printer.move_to,
                args=(None, None, 120, 4000),
                description="Retract head"
            ))


