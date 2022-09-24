from django.db import models
import qrcode, os
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from datetime import datetime

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
    approve_user = models.CharField(max_length=10000, null=True)
    update_by = models.DateField()
    schedule_plan = models.DateField()
    vote_star  = models.IntegerField(null=True)
    vote_percent = models.IntegerField(null=True)
    vote_status = models.CharField(max_length=10000, null=True)
    updated = models.DateField(default=datetime.now)
    expired1 = models.BooleanField(default=False)
    expired2 = models.BooleanField(default=False)
    expired3 = models.BooleanField(default=False)
    expired4 = models.BooleanField(default=False)
    expired5 = models.BooleanField(default=False)

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
            'approve_user': self.approve_user,
            'update_by': self.update_by,
            'schedule_plan': self.schedule_plan,
            'vote_star':  self.vote_star,
            'vote_percent': self.vote_percent,
            'vote_status': self.vote_status,
            'updated': self.updated,
            'expired1': self.expired1,
            'expired2': self.expired2,
            'expired3': self.expired3,
            'expired4': self.expired4,
            'expired5': self.expired5,
        }    
        
class company_backup(models.Model):
    userid = models.IntegerField(null=True)
    updated = models.DateField()
    schedule_plan = models.DateField()
    vote_star  = models.IntegerField(null=True)
    vote_percent = models.IntegerField(null=True)
    vote_status = models.CharField(max_length=10000, null=True)
    
    class Meta:
        db_table = "company_backup"
        
    def to_dict_json(self):
        return {
            'userid': self.userid,
            'updated': self.updated,
            'vote_star': self.vote_star,
            'vote_percent': self.vote_percent,
            'vote_status': self.vote_status,
            'schedule_plan': self.schedule_plan,
        }

class company_qrcode(models.Model):
    userid = models.IntegerField(null=True)
    name = models.CharField(max_length=200)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        qr = qrcode.QRCode(box_size=10, border=1)
        qr.add_data(self.name)
        qr.make(fit=True)
        qrcode_img = qr.make_image()    
        cwd =  os.path.join(os.getcwd(), 'apps/static/media/qr_codes')
        
        if os.path.exists(f'{cwd}/qrcode-{self.name}.png'):
            os.remove(f'{cwd}/qrcode-{self.name}.png')
            
        fname = f'qrcode-{self.name}.png' 
        buffer = BytesIO()
        qrcode_img.save(buffer,'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        super().save(*args, **kwargs)
        
    class Meta:
        db_table = "company_qrcode"
        
        
class username(models.Model):
    name = models.CharField(max_length = 150)
    
    class Meta:
        db_table = "username"
        
    def __str__(self):
        return  str(self.name)
        
        
class thai_province(models.Model): 
    key = models.CharField(max_length=150, null=False)
    province = models.CharField(max_length=150, null=False)
    
    class Meta:
        db_table = "thai_province"
        
        
class thai_district(models.Model): 
    key = models.IntegerField(null=False)
    district_id = models.IntegerField(null=False)
    district = models.CharField(max_length=150, null=False)
    
    class Meta:
        db_table = "thai_district"
        
        
class thai_sub_district(models.Model): 
    key = models.IntegerField(null=False)
    district_id = models.IntegerField(null=False)
    sub_district = models.CharField(max_length=150, null=False)
    
    class Meta:
        db_table = "thai_sub_district"
        
        
class thai_postcode(models.Model): 
    key = models.IntegerField(null=False)
    district_id = models.IntegerField(null=False)
    postcode = models.CharField(max_length=150, null=False)
    
    class Meta:
        db_table = "thai_postcode"
