from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from app.parse.parse import fetch_data

def start_scheduler():
    print("Scheduler started!")
    fetch_data()
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        fetch_data,
        trigger='interval',
        days=3
    )
    scheduler.start()
