# from apscheduler.schedulers.background import BackgroundScheduler
# from .views import run_scheduled_job


# def start():
#     scheduler = BackgroundScheduler()
    
#     @scheduler.scheduled_job('interval', seconds=10, name='auto_run')
#     def auto_run():
#         run_scheduled_job()
        
#     scheduler.start()