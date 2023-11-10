from apscheduler.schedulers.background import BackgroundScheduler
from .events import eventTimeOut  
from datetime import datetime

sched = BackgroundScheduler()
# Schedule job_function to be called every minute
sched.add_job(eventTimeOut, 'interval', minutes=1)

sched.start()