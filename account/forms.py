
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from .models import Account


class RegistrationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ('email', 'username', 'password1', 'password2',)

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError(f'Email "{email}" is already in use')

    def clean_username(self):
        username = self.cleaned_data.get('username').lower()
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError(f'Username "{username}" is already in use')


class AuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Invalid input - login')


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('email', 'username', )
