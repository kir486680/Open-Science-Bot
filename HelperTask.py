import time 
import logging 

def sleep(seconds : float):
    logging.info(f"Sleeping for {seconds} seconds")
    time.sleep(seconds)