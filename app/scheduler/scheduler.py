from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from app.parse.parse import fetch_data

def start_scheduler():
    print("Scheduler started!")
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        fetch_data,
        trigger='interval',
        seconds=15,
        start_date=datetime.now(),
    )
    scheduler.start()