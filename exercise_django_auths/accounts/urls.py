from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.urls import path, reverse_lazy

from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('fbv/login/', views.login_fbv, name='login-fbv'),
    path('fbv/logout/', views.logout_fbv, name='logout-fbv'),
    path('fbv/register/', views.register_fbv, name='register-fbv'),
    path('cbv/login', LoginView.as_view(template_name='accounts/login.html'), name='login-cbv'),
    path('cbv/logout', LogoutView.as_view(), name='logout-cbv'),
    path('cbv/register/', views.RegisterView.as_view(), name='register-cbv'),
    path('details/', views.ProfileDetailView.as_view(), name='detail'),
    path('set-unusable-password/', views.set_unusable_password, name='set-unusable-password'),
    path('password-change/',PasswordChangeView.as_view(
        template_name='accounts/password-change.html',
        success_url=reverse_lazy('accounts:password_change_done')), name='password-change'),
    path('password-change-done/', PasswordChangeDoneView.as_view(template_name='accounts/password-change-done.html'), name='password-change-done'),

]