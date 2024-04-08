from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import BroadcastNotification, company_profile, company_notice
from django.core import serializers
from django.shortcuts import get_object_or_404
import json
import datetime
import asyncio
from celery import Celery, states
from celery.exceptions import Ignore
from django_celery_beat.models import PeriodicTask


def calculate_rating(vote_star):
    if vote_star == 7:  # 5 star point
        vote_status = "Fantastic"
    elif vote_star == 6:  # 4.5 star point
        vote_status = "Excellent"
    elif vote_star == 5:  # 4 star point
        vote_status = "Great"
    elif vote_star == 4:  # 3.5 star point
        vote_status = "Good"
    elif vote_star == 3:  # 3 star point
        vote_status = "Okay"
    elif vote_star == 2:  # 2 star point
        vote_status = "Fair"
    elif vote_star == 1:  # 1 star point
        vote_status = "Please call us"
    else:
        vote_status = "Bad"

    vote_percent = (100 * vote_star) / 7

    return vote_percent, vote_status


@shared_task(bind=True)
def broadcast_realtime(self):
    try:
        qs = company_profile.objects.all()
        # [{'userid': qs_json.userid, 'comoany_name': qs_json.company_name} for qs_json in qs]
        message = json.dumps(
            [
                {
                    "feed": qs_json.feed,
                    "userid": qs_json.userid,
                    "company_name": qs_json.company_name,
                    "job_id": qs_json.job_id,
                    #    'approve_user': qs_json.approve_user,
                    #    'set_date': qs_json.end_date,
                    #    'schedule_plan': qs_json.schedule_plan,
                    #    'dual_date': qs_json.dual_date,
                    "vote": qs_json.vote_star,
                }
                for qs_json in qs
            ]
        )

        channel_layer = get_channel_layer()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(
            channel_layer.group_send(
                "realtime_broadcast", {"type": "send_realtime", "message": message}
            )
        )

        return "Done"
    except:
        self.update_state(
            state="FAILURE",
            meta={
                "exe": "Failed"
                # 'exc_type': type(ex).__name__,
                # 'exc_message': traceback.format_exc().split('\n')
                # 'custom': '...'
            },
        )
        raise Ignore()


@shared_task(bind=True)
def broadcast_notification(self, data):
    try:
        notification = BroadcastNotification.objects.filter(id=int(data))
        if len(notification) > 0:
            notification = notification.first()
            message = json.dumps(notification.message)

            channel_layer = get_channel_layer()
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(
                channel_layer.group_send(
                    "notification_broadcast",
                    {"type": "send_notification", "message": json.dumps(message)},
                )
            )
            notification.sent = True
            notification.save()
            return "Done"
        else:
            self.update_state(state="FAILURE", meta={"exe": "Not Found"})
            raise Ignore()
    except:
        self.update_state(
            state="FAILURE",
            meta={
                "exe": "Failed"
            },
        )
        raise Ignore()


@shared_task(bind=True)
def push_message_job(self):
    
    # date_now = datetime.date.today() + datetime.timedelta(days=1)
    date_now = datetime.date.today()
    model_profile = company_profile.objects.filter(
        end_date__lte=date_now, feed=True
    ).values() 
    
    for instance in model_profile:
        userid = instance["userid"]
        company_name = instance["company_name"]
        job_id = instance["job_id"]
        end_date = datetime.datetime.strptime(str(instance["end_date"]), "%Y-%m-%d")
        schedule_plan = (end_date.date() - date_now).days
        
        if schedule_plan != 0:
            vote_percent = int(instance["vote_percent"] - instance["avg_vote"])
            if vote_percent >= 0:
                vote_star = int((7 * vote_percent) / 100)
            else:
                vote_percent = 0
                vote_star = 0
            _, vote_status = calculate_rating(vote_star)
        else:
            vote_percent = 0
            vote_star = 0
            _, vote_status = calculate_rating(vote_star)
            
        # for company_profile
        obj_cp = get_object_or_404(company_profile, userid=userid)
        obj_cp.vote_star = vote_star
        obj_cp.vote_percent = vote_percent
        obj_cp.vote_status = vote_status
        obj_cp.save()

        # for company_notice
        if vote_star <= 3:
            obj_cn, created_cn = company_notice.objects.get_or_create(
                userid=userid,
                defaults={
                    "userid": userid,
                    "company_name": company_name,
                    "job_id": job_id,
                    "schedule_plan": schedule_plan,
                    "end_date": end_date,
                    "vote_star": vote_star,
                    "vote_percent": vote_percent,
                    "vote_status": vote_status,
                    "expired": True,
                },
            )

            if not created_cn:
                if vote_star != obj_cn.vote_star:
                    obj_cn.expired = True
                    name = f"broadcast-notification-{str(userid)}"
                    tasks = get_object_or_404(PeriodicTask, name=name)
                    tasks.enabled = True
                    tasks.save()
                obj_cn.company_name = company_name
                obj_cn.job_id = job_id
                obj_cn.end_date = end_date
                obj_cn.schedule_plan = schedule_plan
                obj_cn.vote_star = vote_star
                obj_cn.vote_percent = vote_percent
                obj_cn.vote_status = vote_status
                obj_cn.save()
            else:
                BroadcastNotification.objects.update_or_create(
                    userid=userid,
                    defaults={
                        "userid": userid,
                        "message": f"You received notifications userid ({userid}), from {company_name} is expired !!",
                        "broadcast_on": datetime.datetime.now(),
                    },
                )
    return "completed"
