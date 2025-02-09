from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from myapp.tasks import refresh_cache_task

def delete_old_job_executions(max_age=604_800):
    """
    Xóa các lịch sử công việc cũ hơn max_age giây.
    Mặc định là 7 ngày.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # Thêm công việc tự động làm mới cache
    scheduler.add_job(
        refresh_cache_task,
        trigger=CronTrigger(hour=0, minute=0),  # Chạy mỗi ngày lúc 00:00
        id="refresh_cache_task",  # ID duy nhất của công việc
        replace_existing=True,
    )
    print("Added job: refresh_cache_task")

    # Xóa lịch sử công việc cũ mỗi tuần một lần (thứ Hai lúc 00:00)
    scheduler.add_job(
        delete_old_job_executions,
        trigger=CronTrigger(day_of_week="mon", hour=0, minute=0),
        id="delete_old_job_executions",
        replace_existing=True,
    )
    print("Added weekly job: delete_old_job_executions")

    scheduler.start()
    print("Scheduler started")
