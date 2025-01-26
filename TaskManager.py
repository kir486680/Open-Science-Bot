import logging

class TaskManager:
    def __init__(self):
        self.tasks = []
    
    def add_task(self, task):
        self.tasks.append(task)
    
    def run(self):
        logging.info(f"Running {len(self.tasks)} tasks")
        for task in self.tasks:
            # Ensure task.function is a callable
            if callable(task.function):
                logging.info(f"Executing task: {task.function.__name__}")
                task.execute()
            else:
                logging.error("Task function is not callable")
                # Handle result or errors if necessary