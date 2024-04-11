import json
import datetime
from django import template

from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import get_object_or_404

from apps.home.models import (
    company_profile,
    company_notice,
    company_qrcode,
    username,
    BroadcastNotification,
)
from apps.home.forms import company_form

from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django_celery_beat.models import PeriodicTask
from .tasks import push_message_job, calculate_rating


# Create your views here.
def test(request):
    push_message_job.delay()
    return HttpResponse("Done")


@method_decorator(login_required(login_url="/login/"), name="dispatch")
class indexiew(View):
    @csrf_exempt
    def get(self, request):
        try:
            count = company_notice.objects.filter(expired=True).count()
            context = {"segment": "index", "room_name": "broadcast", "count": count}
            html_template = loader.get_template("home/index.html")
            return HttpResponse(html_template.render(context, request))

        except template.TemplateDoesNotExist:
            html_template = loader.get_template("home/page-404.html")
            return HttpResponse(html_template.render(context, request))
        except:
            html_template = loader.get_template("home/page-500.html")
            return HttpResponse(html_template.render(context, request))


@method_decorator(login_required(login_url="/login/"), name="dispatch")
class page_userview(View):
    form_class = company_form
    page = ""

    @csrf_exempt
    def get(self, request, userid=None):
        if userid is None:
            # add
            try:
                model = {"userid": company_profile.objects.latest("userid").userid + 1}
            except company_profile.DoesNotExist:
                userid = 1
                model = {"userid": userid}

            select_user = username.objects.values("name")
            count = company_notice.objects.filter(expired=True).count()

            context = {
                "segment": "page-user",
                "room_name": "broadcast",
                "model": model,
                "select_user": select_user,
                "count": count,
            }
            self.page = "home/page-user.html"

        else:
            # update
            model = get_object_or_404(company_profile, userid=userid)
            select_user = username.objects.values("name")
            count = company_notice.objects.filter(expired=True).count()

            context = {
                "segment": "page-user",
                "room_name": "broadcast",
                "model": model,
                "select_user": select_user,
                "count": count,
            }
            self.page = "home/page-user-edit.html"

        try:
            html_template = loader.get_template(self.page)
            return HttpResponse(html_template.render(context, request))
        except template.TemplateDoesNotExist:
            html_template = loader.get_template("home/page-404.html")
            return HttpResponse(html_template.render(context, request))
        except:
            html_template = loader.get_template("home/page-500.html")
            return HttpResponse(html_template.render(context, request))

    @csrf_exempt
    def post(self, request, userid=None):
        form_data_dict = {}
        form_data_list = json.loads(self.request.POST.get("request"))
        form_data_dict = {field["name"]: field["value"] for field in form_data_list}
        # add new data
        if userid is None:
            try:
                form_data_dict["userid"] = (
                    company_profile.objects.latest("userid").userid + 1
                )
            except company_profile.DoesNotExist:
                form_data_dict["userid"] = 1

            vote_star = int(form_data_dict["vote_star"])
            vote_percent, vote_status = calculate_rating(vote_star)
            form_data_dict["vote_percent"] = int(vote_percent)
            form_data_dict["vote_status"] = vote_status
            form_data_dict["cost"] = int(form_data_dict["cost"])
            form_data_dict["percent_cost"] = int(form_data_dict["percent_cost"])
            form_data_dict["discount"] = int(form_data_dict["discount"])
            form_data_dict["schedule_plan"] = int(form_data_dict["schedule_plan"])
            form_data_dict["start_date"] = datetime.date.today().strftime("%Y-%m-%d")
            form_data_dict["end_date"] = datetime.datetime.strptime(
                form_data_dict["start_date"], "%Y-%m-%d"
            ) + datetime.timedelta(days=int(form_data_dict["schedule_plan"]))
            form_data_dict["avg_vote"] = vote_percent / int(
                form_data_dict["schedule_plan"]
            )
            form = self.form_class(form_data_dict)

            qr_user = form_data_dict["userid"]
            company_qrcode.objects.update_or_create(
                userid=qr_user,
                defaults={
                    "userid": qr_user,
                    "name": f"iaq-tracking-app-d375cd4c464e.herokuapp.com/qr-code/{qr_user}",
                },
            )
            if form.is_valid():
                form.save()

        else:
            # update data
            record = get_object_or_404(company_profile, userid=userid)
            if (
                (record.vote_star == int(form_data_dict["vote_star"]))
                and (record.schedule_plan == int(form_data_dict["schedule_plan"]))
                and (record.end_date == form_data_dict["start_date"])
            ):
                vote_star = record.vote_star
                vote_percent = record.vote_percent
                vote_status = record.vote_status
                avg_vote = record.avg_vote
            else:
                vote_star = int(form_data_dict["vote_star"])
                vote_percent, vote_status = calculate_rating(vote_star)
                avg_vote = vote_percent / int(form_data_dict["schedule_plan"])

            record.company_name = form_data_dict["company_name"]
            record.telephone = form_data_dict["telephone"]
            record.address = form_data_dict["address"]
            record.province = form_data_dict["province"]
            record.district = form_data_dict["district"]
            record.sub_district = form_data_dict["sub_district"]
            record.postal_code = form_data_dict["postal_code"]
            record.job_id = form_data_dict["job_id"]
            record.cost = int(form_data_dict["cost"])
            record.percent_cost = int(form_data_dict["percent_cost"])
            record.discount = int(form_data_dict["discount"])
            record.approve_user = form_data_dict["approve_user"]
            record.start_date = datetime.datetime.strptime(
                form_data_dict["start_date"], "%Y-%m-%d"
            )
            record.end_date = record.start_date + datetime.timedelta(
                days=int(form_data_dict["schedule_plan"])
            )
            record.schedule_plan = int(form_data_dict["schedule_plan"])
            record.avg_vote = avg_vote
            record.vote_star = vote_star
            record.vote_percent = vote_percent
            record.vote_status = vote_status
            record.save()

            notice = company_notice.objects.filter(userid=userid).exists()
            if notice:
                notices = get_object_or_404(company_notice, userid=userid)
                if (
                    (notices.vote_star < record.vote_star)
                    or (
                        (notices.schedule_plan != record.schedule_plan)
                        and (notices.vote_star != record.vote_star)
                    )
                    or (record.vote_star > 3)
                ):
                    notices.delete()

                    name = f"broadcast-notification-{str(userid)}"
                    tasks = get_object_or_404(PeriodicTask, name=name)
                    tasks.delete()

                    broad = get_object_or_404(BroadcastNotification, userid=userid)
                    broad.delete()
                else:
                    notices.company_name = record.company_name
                    notices.job_id = record.job_id
                    notices.end_date = record.end_date
                    notices.schedule_plan = record.schedule_plan
                    notices.save()

        form_data_dict["url"] = "/ui-tables/"
        return JsonResponse(form_data_dict)


@method_decorator(login_required(login_url="/login/"), name="dispatch")
class page_copyview(View):
    form_class = company_form
    page = ""

    @csrf_exempt
    def get(self, request, userid=None):

        if userid is None:
            try:
                userid = company_profile.objects.latest("userid").userid
                model = get_object_or_404(company_profile, userid=userid)
            except company_profile.DoesNotExist:
                pass
            select_user = username.objects.values("name")
            count = company_notice.objects.filter(expired=True).count()

            context = {
                "segment": "page-user",
                "room_name": "broadcast",
                "model": model,
                "select_user": select_user,
                "count": count,
            }
            self.page = "home/page-user-copy.html"

            try:
                html_template = loader.get_template(self.page)
                return HttpResponse(html_template.render(context, request))
            except template.TemplateDoesNotExist:
                html_template = loader.get_template("home/page-404.html")
                return HttpResponse(html_template.render(context, request))
            except:
                html_template = loader.get_template("home/page-500.html")
                return HttpResponse(html_template.render(context, request))

    @csrf_exempt
    def post(self, request, userid=None):
        form_data_dict = {}
        form_data_list = json.loads(self.request.POST.get("request"))
        form_data_dict = {field["name"]: field["value"] for field in form_data_list}
        if userid is None:
            try:
                form_data_dict["userid"] = (
                    company_profile.objects.latest("userid").userid + 1
                )
            except company_profile.DoesNotExist:
                form_data_dict["userid"] = 1

            # vote_star = 0
            vote_percent, vote_status = calculate_rating(
                int(form_data_dict["vote_star"])
            )
            form_data_dict["vote_percent"] = int(vote_percent)
            form_data_dict["vote_status"] = vote_status
            form_data_dict["cost"] = int(form_data_dict["cost"])
            form_data_dict["percent_cost"] = int(form_data_dict["percent_cost"])
            form_data_dict["discount"] = int(form_data_dict["discount"])
            form_data_dict["schedule_plan"] = int(form_data_dict["schedule_plan"])
            form_data_dict["end_date"] = datetime.datetime.strptime(
                form_data_dict["start_date"], "%Y-%m-%d"
            ) + datetime.timedelta(days=int(form_data_dict["schedule_plan"]))

            form_data_dict["avg_vote"] = vote_percent / int(
                form_data_dict["schedule_plan"]
            )
            form = self.form_class(form_data_dict)

            qr_user = form_data_dict["userid"]
            company_qrcode.objects.update_or_create(
                userid=qr_user,
                defaults={
                    "userid": qr_user,
                    "name": f"iaq-tracking-app-d375cd4c464e.herokuapp.com/qr-code/{qr_user}",
                },
            )

            if form.is_valid():
                form.save()

        form_data_dict["url"] = "/copy-user/"
        return JsonResponse(form_data_dict)


@method_decorator(login_required(login_url="/login/"), name="dispatch")
class ui_tablesview(View):
    @csrf_exempt
    def get(self, request):
        model = company_profile.objects.all().order_by("userid")
        qrcode = company_qrcode.objects.all()
        count = company_notice.objects.filter(expired=True).count()

        try:
            context = {
                "segment": "ui-tables",
                "room_name": "broadcast",
                "model": model,
                "qrcode": qrcode,
                "count": count,
            }

            html_template = loader.get_template("home/ui-tables.html")
            return HttpResponse(html_template.render(context, request))
        except template.TemplateDoesNotExist:
            html_template = loader.get_template("home/page-404.html")
            return HttpResponse(html_template.render(context, request))
        except:
            html_template = loader.get_template("home/page-500.html")
            return HttpResponse(html_template.render(context, self.request))

    @csrf_exempt
    def post(self, request, userid=None):
        data = {"segment": "ui-tables"}
        if self.request.POST.get("checked") == "true":
            checked = True
        else:
            checked = False

        record = get_object_or_404(company_profile, userid=userid)
        record.feed = checked
        record.save()

        notice = company_notice.objects.filter(userid=userid).exists()
        if notice:
            notice = get_object_or_404(company_notice, userid=userid)
            notice.expired = checked
            notice.save()

            # count notice
            count = company_notice.objects.filter(expired=True).count()
            data["count"] = count

            name = f"broadcast-notification-{str(userid)}"
            tasks = get_object_or_404(PeriodicTask, name=name)
            tasks.enabled = checked
            tasks.save()

        else:
            count = company_notice.objects.filter(expired=True).count()
            data["count"] = count

        return JsonResponse(data)


@method_decorator(login_required(login_url="/login/"), name="dispatch")
class ui_noticview(View):
    @csrf_exempt
    def get(self, request, userid=None):
        model = company_notice.objects.all().order_by("userid")
        count = company_notice.objects.filter(expired=True).count()
        try:
            context = {
                "segment": "ui-notic",
                "room_name": "broadcast",
                "model": model,
                "count": count,
            }

            html_template = loader.get_template("home/ui-notic.html")
            return HttpResponse(html_template.render(context, request))
        except template.TemplateDoesNotExist:
            html_template = loader.get_template("home/page-404.html")
            return HttpResponse(html_template.render(context, request))
        except:
            html_template = loader.get_template("home/page-500.html")
            return HttpResponse(html_template.render(context, self.request))

    # @csrf_exempt
    # def post(self, request, userid=None):
    #     data = {"segment": "ui-notic"}
    #     if self.request.POST.get("checked") == "true":
    #         checked = True
    #     else:
    #         checked = False

    #     record = get_object_or_404(company_notice, userid=userid)
    #     record.expired = checked
    #     record.save()

    #     # count notice
    #     count = company_notice.objects.filter(expired=True).count()
    #     data["count"] = count

    #     name = f"broadcast-notification-{str(userid)}"
    #     tasks = get_object_or_404(PeriodicTask, name=name)
    #     tasks.enabled = checked
    #     tasks.save()

    #     return JsonResponse(data)


def delete_userview(request, userid=None):
    context = dict()
    model = get_object_or_404(company_profile, userid=userid)
    qrcode = get_object_or_404(company_qrcode, userid=userid)

    try:
        notice = company_notice.objects.filter(userid=userid).exists()
        if notice:
            notice = get_object_or_404(company_notice, userid=userid)
            notice.delete()

            name = f"broadcast-notification-{str(userid)}"
            tasks = get_object_or_404(PeriodicTask, name=name)
            tasks.delete()

            broad = get_object_or_404(BroadcastNotification, userid=userid)
            broad.delete()

    except company_notice.DoesNotExist:
        html_template = loader.get_template("home/page-404.html")
        return HttpResponse(html_template.render(context, request))

    context = {
        "resp": True,
        "userid": model.userid,
        "company_name": model.company_name,
    }

    try:
        model.delete()
        qrcode.delete()
    except:
        context["resp"] = False

    return JsonResponse(context)


class qrcodeview(View):

    @csrf_exempt
    def get(self, request, userid=None):
        count = company_notice.objects.filter(expired=True).count()

        if userid is None:
            context = {"segment": "ui-tables"}
        else:
            model = get_object_or_404(company_profile, userid=userid)
            qrcode = get_object_or_404(company_qrcode, userid=userid)
            context = {
                "segment": "qr-code",
                "room_name": "broadcast",
                "model": model,
                "qrcode": qrcode,
                "count": count,
            }

            if self.request.GET.get("request") is not None:
                qr_type_value = self.request.GET.get("request")
                update = get_object_or_404(company_profile, userid=userid)
                update.qr_type = qr_type_value
                update.save()
        try:
            html_template = loader.get_template("home/test.html")
            return HttpResponse(html_template.render(context, request))
        except template.TemplateDoesNotExist:
            html_template = loader.get_template("home/page-404.html")
            return HttpResponse(html_template.render(context, request))
        except:
            html_template = loader.get_template("home/page-500.html")
            return HttpResponse(html_template.render(context, request))

    @csrf_exempt
    def post(self, request, userid=None):
        model = get_object_or_404(company_profile, userid=userid)
        qrcode = get_object_or_404(company_qrcode, userid=userid)
        data = {
            "company_name": model.company_name,
            "job_id": model.job_id,
            "qr_type": model.qr_type,
            "qrcode": qrcode.qr_code.url,
        }

        return JsonResponse(data)
