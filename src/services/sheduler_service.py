from datetime import datetime
from aiogram.fsm.context import FSMContext
from src.data.config import settings
from src.services.user_service import UserService
from src.utils.database.uow import InitUoW
from src.utils.loader import scheduler
from apscheduler.job import Job
from apscheduler.schedulers import SchedulerAlreadyRunningError

class ShedulerService:
    @staticmethod
    async def add_reminders_job(func, user_id: int, state: FSMContext, day: int):
        job_id = f'remind_{settings.REMINER1_SECONDS}_' + str(user_id)
        scheduler.add_job(
            func,
            'interval',
            seconds=settings.REMINER1_SECONDS,
            args=[user_id, job_id, day],
            id=job_id
        )
        job_id = f'remind_{settings.REMINER2_SECONDS}_' + str(user_id)
        scheduler.add_job(
            func,
            'interval',
            seconds=settings.REMINER2_SECONDS,
            args=[user_id, job_id, day],
            id=job_id
        )
        job_id = f'remind_{settings.REMINER3_SECONDS}_' + str(user_id)
        scheduler.add_job(
            func,
            'interval',
            seconds=settings.REMINER3_SECONDS,
            args=[user_id, job_id, day],
            id=job_id
        )
        await state.update_data({
            f"remind_{day}": 0
        })
        scheduler.print_jobs()
        try:
            scheduler.start()
        except SchedulerAlreadyRunningError:
            print("The scheduler is already running")

    @staticmethod
    def delete_user_jobs(user_id: int):
        user_id = str(user_id)
        jobs: list[Job]= scheduler.get_jobs()
        print(jobs, 'jobsjobs')
        print(type(jobs))
        for job in jobs:
            if job.id.count(user_id):
                print(job.id)
                scheduler.remove_job(job_id=job.id)
    
    @staticmethod
    async def add_main_job(func, user_id: int, uow: InitUoW):
        # scheduler.add_job(
        #     send_daily_prediction_message,
        #     CronTrigger(
        #         hour=current_time.hour,
        #         minute=current_time.minute,
        #         second=current_time.second,
        #     ), args=[user_id, uow]
        # )
        jobs: list[Job]= scheduler.get_jobs()
        print(jobs, 'jobsjobs')
        print(type(jobs))
        for job in jobs:
            if job.id == str(user_id):
                scheduler.remove_job(job_id=str(user_id))

        scheduler.add_job(
            func,
            'interval',
            # hours=8,
            minutes=2,
            args=[user_id],
            id=str(user_id)
        )
        try:
            scheduler.start()
        except SchedulerAlreadyRunningError:
            print("The scheduler is already running")
        current_time=datetime.now().time()
        await UserService.add_sheduler_time(
            user_id=user_id,
            sheduler_time=current_time,
            uow=uow
        )
        # await GSheetService.update_user_data(
        #     tg_id=user_id,
        #     day=1,
        #     with_current_time=True
        # )
    @staticmethod
    async def update_recommendations(func):
        job_id = 'recommendations'
        # print(scheduler.get_jobs(jobstore=jobstores['default']))
        # existing_job = scheduler.get_job(job_id)
        # print(existing_job, 'fadsfdafdf')
        # if existing_job:
        #     scheduler.remove_job(job_id)
        scheduler.add_job(
            func,
            'cron',
            hour=settings.recommendation_hour,
            minute=settings.recommendation_minute,
            id=job_id,
            replace_existing=True
        )
       
        try:
            scheduler.start()
        except SchedulerAlreadyRunningError:
            print("The scheduler is already running")
            
    @staticmethod
    async def update_moon_data(func):
        job_id = 'moon_data'
        # existing_job = scheduler.get_job(job_id)
        # if existing_job:
        #     scheduler.remove_job(job_id)
        scheduler.add_job(
            func,
            'cron',
            hour=settings.moon_data_hour,
            minute=settings.moon_data_minute,
            id=job_id,
            replace_existing=True
        )
        
        try:
            scheduler.start()
        except SchedulerAlreadyRunningError:
            print("The scheduler is already running")
  