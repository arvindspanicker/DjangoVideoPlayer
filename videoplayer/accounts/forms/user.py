from django.contrib.auth.forms import UserChangeForm , UserCreationForm

from accounts.models import UserModel
from .base import BaseLoggedForm

class UserForm(BaseLoggedForm):

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'enter username ...'
        self.fields['first_name'].widget.attrs['placeholder'] = 'enter first name ...'
        self.fields['last_name'].widget.attrs['placeholder'] = 'enter last name ...'
        self.fields['email'].required = True
        self.fields['email'].widget.attrs['placeholder'] = 'enter email ...'

    class Meta:
        model = UserModel
        fields = ['username', 'first_name', 'last_name', 'email', 'active', 'is_admin']


class UserAdminForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = UserModel

class UserSignUpForm(UserCreationForm):


    def __init__(self, *args, **kwargs):
        super(UserSignUpForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = UserModel
        fields = ('username', 'email','first_name','last_name','password1', 'password2')
