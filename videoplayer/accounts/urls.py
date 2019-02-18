from django.contrib.auth import views
from django.conf.urls import url

urlpatterns = [
    url('login/', views.LoginView.as_view(), name='login'),
    url('logout/', views.LogoutView.as_view(), name='logout'),

    url('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    url('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    url('password_reset/', views.PasswordResetView.as_view(),
         name='password_reset'),
    url('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url('reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]