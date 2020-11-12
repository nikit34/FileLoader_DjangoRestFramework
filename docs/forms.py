from django import forms
from .models import Doc


class UploadForm(forms.ModelForm):
    upload = forms.FileField()

    class Meta:
        model = Doc
        fields = ('upload',)

    def clean_upload(self, *args, **kwargs):
        upload = self.cleaned_data.get('upload')
        if upload.size > 5242880:
            raise forms.ValidationError("File must be before 5mb")
        return upload