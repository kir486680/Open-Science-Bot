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
    