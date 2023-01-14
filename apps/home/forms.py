from django import forms
from apps.home.models import company_profile, username, company_qrcode

class company_form(forms.ModelForm):
        
    userid = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))
    company_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))
    
    address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))
    
    telephone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))
    
    job_id = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))
    
    cost = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control"
            }
        ))
    
    percent_cost = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control"
            }
        ))
    
    discount = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control"
            }
        ))
    
    approve_user = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))
    
    start_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date"
            }
        ))
    
    end_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date"
            }
        ))
    
    schedule_plan = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control"
            }
        ))
    
    dual_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date"
            }
        ))
            
    vote_star = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control"
            }
        ))
    
    vote_percent = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control"
            }
        ))

    vote_status = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))
    
    district = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))
    
    sub_district = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))
    
    province = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))
    
    postal_code = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))
    
    class Meta:
        model = company_profile
        fields= ('userid', 'company_name', 'address', 'telephone',
                'district', 'sub_district', 'province', 'postal_code',
                'job_id', 'cost', 'percent_cost', 'discount',
                'approve_user', 'start_date', 'end_date', 'schedule_plan', 'dual_date',
                'avg_vote','vote_star', 'vote_percent', 'vote_status')

class username_form(forms.ModelForm):    
    class Meta:
        model = username
        fields = ("name",)