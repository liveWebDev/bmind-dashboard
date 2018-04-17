"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, User
from django.utils.translation import ugettext_lazy as _
from app.models import UserProfileInfo

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','email','password')


class UserProfileInfoForm(forms.ModelForm):
    picture = forms.ImageField(required=False)

    class Meta():
        model = UserProfileInfo
        fields = ('profile_pic',)

# class BootstrapAuthenticationForm(AuthenticationForm):
#     """Authentication form which uses boostrap CSS."""
#     username = forms.CharField(max_length=254,
#                                widget=forms.TextInput({
#                                    'class': 'form-control',
#                                    'placeholder': '',
#                                    'background-color': '#f2f2f2'}))
#
#     password = forms.CharField(label=_("Password"),
#                                widget=forms.PasswordInput({
#                                    'class': 'form-control',
#                                    'placeholder': '',
#                                    'background-color': '#f2f2f2'}))
