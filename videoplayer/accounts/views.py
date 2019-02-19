from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from django.views.generic.edit import FormView

from accounts.forms import UserSignUpForm

class UserSignUp(FormView):
    form_class = UserSignUpForm
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        form.save()
        return redirect('login')
