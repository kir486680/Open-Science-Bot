import time 
import logging 

def sleep(seconds : float):
    """
    Sleeps for a given number of seconds
    """
    logging.info(f"Sleeping for {seconds} seconds")
    time.sleep(seconds)