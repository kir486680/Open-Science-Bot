import logging
from typing import List, Optional
from contextlib import contextmanager
from Task import Task


class TaskManager:
    def __init__(self):
        self.tasks: List[Task] = []
        self.current_sequence: Optional[List[Task]] = None
    
    @contextmanager
    def sequence(self, name: str):
        """Create a named sequence of tasks"""
        self.current_sequence = []
        yield
        if self.current_sequence:
            logging.info(f"Adding sequence: {name} with {len(self.current_sequence)} tasks")
            self.tasks.extend(self.current_sequence)
        self.current_sequence = None
    
    def add_task(self, task: Task) -> None:
        if self.current_sequence is not None:
            self.current_sequence.append(task)
        else:
            self.tasks.append(task)
    
    def execute_all(self) -> None:
        """Execute all tasks in the queue"""
        logging.info(f"Executing {len(self.tasks)} tasks")
        for i, task in enumerate(self.tasks):
            try:
                logging.info(f"Task {i+1}/{len(self.tasks)}: {task.description or task.function.__name__}")
                task.execute()
            except Exception as e:
                logging.error(f"Failed at task {i+1}: {e}")
                raise
        self.tasks.clear()  # Clear tasks after execution
    
    @contextmanager
    def execute_sequence(self, sequence_name: str) -> None:
        """Execute a specific sequence of tasks immediately"""
        temp_sequence = []
        self.current_sequence = temp_sequence
        try:
            yield
            if temp_sequence:
                logging.info(f"Executing sequence '{sequence_name}' with {len(temp_sequence)} tasks")
                for i, task in enumerate(temp_sequence):
                    try:
                        logging.info(f"Task {i+1}/{len(temp_sequence)}: {task.description}")
                        task.execute()
                    except Exception as e:
                        logging.error(f"Failed at task {i+1} in sequence '{sequence_name}': {e}")
                        raise
        finally:
            self.current_sequence = None
    