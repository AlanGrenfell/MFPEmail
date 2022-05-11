from apscheduler.schedulers.blocking import BlockingScheduler
from main import sendMail

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='sun', hour=8)
def scheduled_job():
    print('This job is run every Sunday 8 AM.')
    sendMail()
sched.start()