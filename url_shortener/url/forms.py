from django import forms
from .models import *

class UrlForm(forms.ModelForm):
    class Meta:    
        model = Url
        fields = ('original_url',)
