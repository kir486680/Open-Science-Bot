import logging

class Task:
    def __init__(self, function, args=None):
        self.function = function
        self.args = args or []
    
    def execute(self):
        try:
            logging.info(f"Args: {self.args}")
            return self.function(*self.args)
        except Exception as e:
            logging.error(f"Error executing task {self.function.__name__}: {e}")
            

