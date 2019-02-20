# Django imports
from django.contrib.auth import views
from django.urls import re_path

# Custom imports
from .views import UserSignUp

urlpatterns = [
    re_path('login', views.LoginView.as_view(), name='login'),
    re_path('logout', views.LogoutView.as_view(), name='logout'),
    re_path('signup', UserSignUp.as_view(), name='signup'),

]