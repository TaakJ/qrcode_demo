from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json

# Create your models here.

class company_profile(models.Model):
    userid = models.IntegerField(null=True)
    company_name = models.CharField(max_length=10000, null=True)
    telephone = models.CharField(max_length=10000)
    address = models.CharField(max_length=10000, null=True)
    district = models.CharField(max_length=150)
    sub_district = models.CharField(max_length=150)
    province = models.CharField(max_length=150)
    postal_code = models.CharField(max_length=150)
    job_id = models.CharField(max_length=10000, null=True)
    cost = models.IntegerField(null=True)
    percent_cost = models.IntegerField(null=True)
    discount = models.IntegerField(null=True)
    approve_user = models.CharField(max_length=10000, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    schedule_plan = models.IntegerField(null=True)
    vote_star  = models.IntegerField(null=True)
    vote_percent = models.IntegerField(null=True)
    vote_status = models.CharField(max_length=10000, null=True)
    qr_type = models.IntegerField(default=1, null=False)
    avg_vote = models.FloatField(null=False)
    feed = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('userid',)
        db_table = "company_profile"
        
    def to_dict_json(self):
        return {
            'userid': self.userid,
            'company_name': self.company_name,
            'telephone': self.telephone,
            'address': self.address,
            'district': self.district,
            'sub_district': self.sub_district,
            'province': self.province,
            'postal_code': self.postal_code,
            'job_id': self.job_id,
            'cost': self.cost,
            'percent_cost': self.percent_cost,
            'discount': self.discount,
            'approve_user': self.approve_user,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'schedule_plan': self.schedule_plan,
            'vote_star':  self.vote_star,
            'vote_percent': self.vote_percent,
            'vote_status': self.vote_status,
            'qr_type': self.qr_type,
            'avg_vote': self.avg_vote,
            'feed': self.feed,
            'updated': self.updated,
        }    
        
class company_notice(models.Model):
    userid = models.IntegerField(null=True)
    company_name = models.CharField(max_length=10000, null=True)
    job_id = models.CharField(max_length=10000, null=True)
    schedule_plan = models.IntegerField(null=True)
    end_date = models.DateField()
    vote_star  = models.IntegerField(null=True)
    vote_percent = models.IntegerField(null=True)
    vote_status = models.CharField(max_length=10000, null=True)
    expired = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "company_notice"
        
    def to_dict_json(self):
        return {
            'userid': self.userid,
            'company_name': self.company_name,
            'job_id': self.job_id,
            'schedule_plan': self.schedule_plan,
            'end_date': self.dual_date,
            'updated': self.updated,
            'vote_star': self.vote_star,
            'vote_percent': self.vote_percent,
            'vote_status': self.vote_status,
            'expired': self.expired,
        }

class company_qrcode(models.Model):
    userid = models.IntegerField(null=True)
    name = models.CharField(max_length=200)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.name)
    
    def save(self, *args, **kwargs):
        qr = qrcode.QRCode(box_size=6, border=2)
        qr.add_data(self.name)
        qr.make(fit=True)
        qrcode_img = qr.make_image(fill_color="black", back_color="white")
        
        fname = f"qrcode-{self.userid}.png"
        _buffer = BytesIO()
        qrcode_img.save(_buffer,'PNG')
        _buffer.seek(0)
        self.qr_code.save(fname, File(_buffer), save=False)
        super().save(*args, **kwargs)
    class Meta:
        db_table = "company_qrcode"

class username(models.Model):
    name = models.CharField(max_length = 150)
    
    class Meta:
        db_table = "username"
        
    def __str__(self):
        return  str(self.name)
    
class BroadcastNotification(models.Model):
    userid = models.IntegerField(null=True)
    message = models.TextField()
    broadcast_on = models.DateTimeField()
    sent = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-broadcast_on']

@receiver(post_save, sender=BroadcastNotification)
def notification_handler(sender, instance, created, **kwargs):
    # call group_send function directly to send notificatoions or you can create a dynamic task in celery beat
    if created:
        schedule, created = CrontabSchedule.objects.get_or_create(
                                                            hour = '*',
                                                            minute = '*/2',
                                                            day_of_month = '*', 
                                                            month_of_year = '*', 
                                                            timezone = "Asia/Bangkok"
                                                        )
    
        PeriodicTask.objects.create(crontab=schedule, 
                                    name="broadcast-notification-"+str(instance.userid), 
                                    task="apps.home.tasks.broadcast_notification", 
                                    args=json.dumps((instance.id,))
                                    )

        
