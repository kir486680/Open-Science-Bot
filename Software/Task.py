import logging
from dataclasses import dataclass
from typing import Callable, Any, Tuple

@dataclass
class Task:
    function: Callable
    args: Tuple[Any, ...] = ()
    description: str = ""
    
    def execute(self) -> Any:
        """
        Executes the task
        """
        try:
            logging.info(f"Executing: {self.description or self.function.__name__}")
            return self.function(*self.args)
        except Exception as e:
            logging.error(f"Error executing {self.function.__name__}: {e}")
            raise