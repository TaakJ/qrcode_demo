from django.contrib import admin
from .models import company_profile, company_qrcode, company_notice, username , BroadcastNotification

# Register your models here.
admin.site.register(company_profile)
admin.site.register(company_notice)
admin.site.register(company_qrcode)
admin.site.register(username)
admin.site.register(BroadcastNotification)