import time 
import logging 

def sleep(seconds):
    logging.info(f"Sleeping for {seconds} seconds")
    time.sleep(seconds)