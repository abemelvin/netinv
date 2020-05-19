from django import forms

from .models import Scan


class ScanForm(forms.ModelForm):

    class Meta:
        model = Scan
        fields = ('username', 'password')
        labels = {'username': 'TACACS username', 'password': 'TACACS password'}