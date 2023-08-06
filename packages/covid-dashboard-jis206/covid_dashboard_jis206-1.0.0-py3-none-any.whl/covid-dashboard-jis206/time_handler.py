"""
Has Utility functions that allows the project to manipulate time values into more usable formats
"""

import time
import logging

FORMAT='%(levelname)s:%(asctime)s:%(message)s'
logging.basicConfig(format=FORMAT,filename='sys.log', encoding='utf-8', level=logging.INFO)

def hhmm_to_seconds_from_now(hhmm: str) -> int:
    """
    Takes a time in the format hh:mm and returns the time until then in seconds
    """

    if len(hhmm.split(':')) != 2:
        logging.error("Time not given in the format 'hh:mm'. Terminating process")
        return
    hrs, mins = map(int,hhmm.split(':'))
    secs = hrs*3600 + mins*60

    now_hhmm = time.strftime("%H:%M")
    now_hrs, now_mins = map(int,now_hhmm.split(':'))
    now_secs = now_hrs*3600 + now_mins*60
    diff = ((24*60*60) + secs - now_secs) % (24*60*60)
    return diff


def seconds_from_now_to_hhmm(seconds_from_now: int) -> str:
    """
    Takes a time in seconds and returns the time at which
    those seconds will elapse in the form of hh:mm
    """
    now_hhmm = time.strftime("%H:%M")
    now_hrs, now_mins = map(int,now_hhmm.split(':'))
    now_secs = now_hrs*3600 + now_mins*60

    secs = (seconds_from_now + now_secs) % (24*60*60)

    mins = secs//60
    hrs = str(mins//60)
    mins = str(mins % 60)
    if len(hrs)==1:
        hrs = "0" + hrs
    if len(mins)==1:
        mins = "0" + mins

    hhmm = f"{hrs}:{mins}"
    return hhmm
