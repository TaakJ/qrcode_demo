import json, datetime, os
from django.utils import timezone

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect,  get_object_or_404

from apps.home.models import company_profile, company_backup, company_qrcode, username, thai_province, thai_district, thai_sub_district, thai_postcode
from apps.home.forms import company_form 

from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def run_scheduled_job():
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    model = company_profile.objects.all()
    
    for doc in model:
        if (doc.schedule_plan.strftime('%Y-%m-%d') <= today) and (doc.expired1 is False):
            print("follow schedule_plan timeout ....")
            vote_star = doc.vote_star - 1
            vote_percent, vote_status = calculate_rating(vote_star)
                
            # insert row to table company_backup
            company_backup.objects.create(userid=doc.userid
                                        ,vote_star=doc.vote_star
                                        ,vote_percent=doc.vote_percent
                                        ,vote_status=doc.vote_status
                                        ,schedule_plan=doc.schedule_plan
                                        ,updated=doc.schedule_plan)
            
            # update expired flag True to table company_profile
            company_profile.objects.filter(userid=doc.userid).update(expired1=True
                                                                    ,vote_percent=vote_percent
                                                                    ,vote_star=vote_star
                                                                    ,vote_status=vote_status
                                                                    ,updated=datetime.datetime.now(tz=timezone.utc))
            
        elif (doc.schedule_plan + datetime.timedelta(1) == today) and (doc.expired1 is True) and (doc.expired2 is False) and (doc.updated.strftime('%Y-%m-%d') != today):
            vote_star = doc.vote_star - 1
            vote_percent, vote_status = calculate_rating(vote_star)
                
            # insert row to table company_backup
            company_backup.objects.create(userid=doc.userid
                                        ,vote_star=doc.vote_star
                                        ,vote_percent=doc.vote_percent
                                        ,vote_status=doc.vote_status
                                        ,schedule_plan=doc.schedule_plan
                                        ,updated=doc.schedule_plan + datetime.timedelta(2))
            
            # update expired flag True to table company_profile
            company_profile.objects.filter(userid=doc.userid).update(expired2=True
                                                                    ,vote_percent=vote_percent
                                                                    ,vote_star=vote_star
                                                                    ,vote_status=vote_status
                                                                    ,updated=datetime.datetime.now(tz=timezone.utc))
            
        elif (doc.schedule_plan + datetime.timedelta(2) == today) and (doc.expired1 is True) and (doc.expired2 is True) and (doc.expired3 is False) and (doc.updated.strftime('%Y-%m-%d') != today):
            vote_star = doc.vote_star - 1
            vote_percent, vote_status = calculate_rating(vote_star)
                
            # insert row to table company_backup
            company_backup.objects.create(userid=doc.userid
                                        ,vote_star=doc.vote_star
                                        ,vote_percent=doc.vote_percent
                                        ,vote_status=doc.vote_status
                                        ,schedule_plan=doc.schedule_plan
                                        ,updated=doc.schedule_plan + datetime.timedelta(14))
            
            # update expired flag True to table company_profile
            company_profile.objects.filter(userid=doc.userid).update(expired3=True
                                                                    ,vote_percent=vote_percent
                                                                    ,vote_star=vote_star
                                                                    ,vote_status=vote_status
                                                                    ,updated=datetime.datetime.now(tz=timezone.utc))
            
        elif (doc.schedule_plan + datetime.timedelta(3) == today) and (doc.expired1 is True) and (doc.expired2 is True) and (doc.expired3 is True) and (doc.expired4 is False) and (doc.updated.strftime('%Y-%m-%d') != today):
            vote_star = doc.vote_star - 1 
            vote_percent, vote_status = calculate_rating(vote_star) 
                
            # insert row to table company_backup
            company_backup.objects.create(userid=doc.userid
                                        ,vote_star=doc.vote_star
                                        ,vote_percent=doc.vote_percent
                                        ,vote_status=doc.vote_status
                                        ,schedule_plan=doc.schedule_plan
                                        ,updated=doc.schedule_plan + datetime.timedelta(3))
            
            # update expired flag True to table company_profile
            company_profile.objects.filter(userid=doc.userid).update(expired4=True
                                                                    ,vote_percent=vote_percent
                                                                    ,vote_star=vote_star
                                                                    ,vote_status=vote_status
                                                                    ,updated=datetime.datetime.now(tz=timezone.utc))
            
        elif (doc.schedule_plan + datetime.timedelta(4) == today) and (doc.expired1 is True) and (doc.expired2 is True) and (doc.expired3 is True)  and (doc.expired4 is True) and (doc.expired5 is False) and (doc.updated.strftime('%Y-%m-%d') != today):
            vote_star = doc.vote_star - 1  
            vote_percent, vote_status = calculate_rating(vote_star)
                
            # insert row to table company_backup
            company_backup.objects.create(userid=doc.userid
                                        ,vote_star=doc.vote_star
                                        ,vote_percent=doc.vote_percent
                                        ,vote_status=doc.vote_status
                                        ,schedule_plan=doc.schedule_plan
                                        ,updated=doc.schedule_plan + datetime.timedelta(4))
            
            # update expired flag True to table company_profile
            company_profile.objects.filter(userid=doc.userid).update(expired5=True
                                                                    ,vote_percent=vote_percent
                                                                    ,vote_star=vote_star
                                                                    ,vote_status=vote_status
                                                                    ,updated=datetime.datetime.now(tz=timezone.utc))
        else:
            print("run_scheduled_job every 1 min..")
            

def calculate_rating(vote_star):
    if vote_star == 5: 
        vote_percent = 100
        vote_status = 'Excellent'
    elif vote_star == 4:
        vote_percent = 80
        vote_status = 'Good'
    elif vote_star == 3:
        vote_percent = 60
        vote_status = 'Fair'
    elif vote_star == 2:
        vote_percent = 40
        vote_status = 'Poor'
    elif vote_star == 1:
        vote_percent = 20
        vote_status = 'Bad'
    else:
        vote_percent = 0
        vote_status = 'Emtry'
    
    return vote_percent, vote_status


class indexiew(View):
    def get(self, request):
        try:
            context = {'segment': 'index'}
            html_template = loader.get_template('home/index.html')
            return  HttpResponse(html_template.render(context, request))
        
        except template.TemplateDoesNotExist:
            html_template = loader.get_template('home/page-404.html')
            return HttpResponse(html_template.render(context, request))
        except:
            html_template = loader.get_template('home/page-500.html')
            return HttpResponse(html_template.render(context, request))

class page_userview(View):
    form_class = company_form
    page = ""
    
    def get(self, request, userid=None): 
        if userid is None:
            # add
            try:
                model = {'userid': company_profile.objects.latest('userid').userid + 1}
            except company_profile.DoesNotExist:
                userid = 1
                model = {'userid': userid}
            
            select_user = username.objects.values('name')
            select_province = thai_province.objects.all()
            select_district = thai_district.objects.all()
            select_sub_district = thai_sub_district.objects.all()
            select_postcode = thai_postcode.objects.all()
            
            context = {
                    'segment': 'page-user',
                    'model': model,
                    'select_user': select_user,
                    'select_province': select_province,
                    'select_district': select_district,
                    'select_sub_district': select_sub_district,
                    'select_postcode': select_postcode
                }
            self.page = 'home/page-user.html'
            
        else:
            # update
            model = get_object_or_404(company_profile, userid=userid)
            select_user = username.objects.values('name')
            select_province = thai_province.objects.all()
            select_district = thai_district.objects.all()
            select_sub_district = thai_sub_district.objects.all()
            select_postcode = thai_postcode.objects.all()

            context = {
                'segment': 'page-user',
                'model': model,
                'select_user': select_user,
                'select_province': select_province,
                'select_district': select_district,
                'select_sub_district': select_sub_district,
                'select_postcode': select_postcode
            }
            self.page = 'home/page-user-edit.html'
            
        try:
            html_template = loader.get_template(self.page)    
            return HttpResponse(html_template.render(context, request))
            
        except template.TemplateDoesNotExist:
            html_template = loader.get_template('home/page-404.html')
            return HttpResponse(html_template.render(context, request))
            
        except:
            html_template = loader.get_template('home/page-500.html')
            return HttpResponse(html_template.render(context, request))
    
    @csrf_exempt
    def post(self, request, userid=None):
        form_data_dict = {}
        form_data_list = json.loads(self.request.POST.get('request'))
        form_data_dict = {field["name"]: field["value"] for field in form_data_list}
        if userid is None:
            try:
                form_data_dict['userid'] = company_profile.objects.latest('userid').userid + 1
            except company_profile.DoesNotExist:
                form_data_dict['userid'] = 1
                
            vote_star = form_data_dict['vote_star']
            vote_percent, vote_status = calculate_rating(int(vote_star))
            form_data_dict['vote_percent'] = int(vote_percent)
            form_data_dict['vote_status'] = vote_status
            form_data_dict['expired'] = False
            form = self.form_class(form_data_dict)
            
            try:
                qr_user = form_data_dict['userid']
                company_qrcode.objects.create(userid=qr_user, name=f'wwww.qrcode-air-quality/qr-code/{qr_user}')
            except company_qrcode.DoesNotExist:
                pass
            
            if form.is_valid():
                form.save()
        else:
            vote_star = int(form_data_dict['vote_star'])
            vote_percent, vote_status = calculate_rating(int(vote_star))
            company_profile.objects.filter(userid=userid).update(
                company_name = form_data_dict['company_name'],
                telephone = form_data_dict['telephone'],
                address = form_data_dict['address'],
                province = form_data_dict['province'],
                district = form_data_dict['district'],
                sub_district = form_data_dict['sub_district'],
                postal_code = form_data_dict['postal_code'],
                approve_user = form_data_dict['approve_user'],
                update_by = form_data_dict['update_by'],
                schedule_plan = form_data_dict['schedule_plan'],
                vote_star = vote_star,
                vote_percent = vote_percent,
                vote_status = vote_status,
                expired1 = False,
                expired2 = False,
                expired3 = False,
                expired4 = False,
                expired5 = False,
            )
            
        form_data_dict['url'] = '/ui-tables/'
        return JsonResponse(form_data_dict)

class ui_tablesview(View):
    def get(self, request):
        model = company_profile.objects.all()
        try:
            context = {'segment': 'ui-tables',
                    'model': model
                    }
            html_template = loader.get_template('home/ui-tables.html')
            return HttpResponse(html_template.render(context, request))
        
        except template.TemplateDoesNotExist:
            html_template = loader.get_template('home/page-404.html')
            return HttpResponse(html_template.render(context, request))
        
        except:
            html_template = loader.get_template('home/page-500.html')
            return HttpResponse(html_template.render(context, self.request))
        
def delete_userview(request, userid=None):
    data = dict()
    model = get_object_or_404(company_profile, userid=userid)
    data = {
        'resp': True,
        'userid': model.userid,
        'company_name': model.company_name
    }
    try:
        model.delete()
        get_object_or_404(company_qrcode, userid=userid).delete()
    except Exception as err:
        data['resp'] = False
    
    return JsonResponse(data)
        
class qrcodeview(View):
    def get(self, request, userid=None):
        if userid is None:
            context = {'segment': 'ui-tables'}
        else:
            model = get_object_or_404(company_profile, userid=userid)
            qrcode = get_object_or_404(company_qrcode, userid=userid)
            context = {
                'segment': 'qr-code',
                'model': model,
                'qrcode':qrcode
            }
        try:
            html_template = loader.get_template('home/test.html')
            return  HttpResponse(html_template.render(context, request))
            
        except template.TemplateDoesNotExist:
            html_template = loader.get_template('home/page-404.html')
            return HttpResponse(html_template.render(context, request))
            
        except:
            html_template = loader.get_template('home/page-500.html')
            return HttpResponse(html_template.render(context, request))
        