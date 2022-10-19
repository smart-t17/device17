from app import db
from apscheduler.schedulers.blocking import BlockingScheduler
from services.device_service import update_devices

"""
cron jobs.For more info look here:
https://apscheduler.readthedocs.io/en/latest/modules/triggers/cron.html
"""

sched = BlockingScheduler(job_defaults={"misfire_grace_time": 15 * 60})


@sched.scheduled_job("cron", minute=0)  # type: ignore
def update_device_history() -> None:
    update_devices()


sched.start()
