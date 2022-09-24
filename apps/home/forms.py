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
    
    approve_user = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))
    
    update_by = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date"
            }
        ))
    
    schedule_plan = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date"
            }
        ))
            
    vote_star = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))
    
    vote_percent = forms.IntegerField(
        widget=forms.TextInput(
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
        fields= ('userid', 'company_name', 'address', 'telephone', 'approve_user', 'update_by', 'schedule_plan', 'vote_star', 'vote_percent', 'vote_status', 'district', 'sub_district', 'province', 'postal_code')

class username_form(forms.ModelForm):    
    class Meta:
        model = username
        fields = ("name",)