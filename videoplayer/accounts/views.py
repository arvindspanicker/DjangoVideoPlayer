# Django imports
from django.shortcuts import redirect
from django.views.generic.edit import FormView

from accounts.forms import UserSignUpForm

class UserSignUp(FormView):
    """
    Custom User Sign Up Class based View
    """
    form_class = UserSignUpForm
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        form.save()
        return redirect('login')
