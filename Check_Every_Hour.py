import schedule
import time
from os import system

def job():
    system("python Price_Tracker.py")


schedule.every(1).hours.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)