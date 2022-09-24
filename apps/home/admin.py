from django.contrib import admin
from .models import company_profile, company_qrcode, company_backup, username

# Register your models here.
admin.site.register(company_profile)
admin.site.register(company_backup)
admin.site.register(company_qrcode)
admin.site.register(username)
# admin.site.register(thai_province)
# admin.site.register(thai_district)
# admin.site.register(thai_sub_district)