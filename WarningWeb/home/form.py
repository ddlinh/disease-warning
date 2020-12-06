from django import forms

class AccountForm(forms.Form):
    location = forms.CharField()