from django import forms
from django.forms import fields
from .models import Doc


class UploadForm(forms.ModelForm):
    class Meta:
        model = Doc
        fields = ('upload',)