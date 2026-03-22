from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import logout_then_login
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from accounts.forms import SetUnusablePasswordForm, CustomUserCreationForm

UserModel = get_user_model()

@user_passes_test(lambda user: not user.is_authenticated)
def register_fbv(request: HttpRequest):
    form = UserCreationForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('home')
    return render(request, 'accounts/register.html', {'form': form})

def login_fbv(request: HttpRequest) -> HttpResponse:
    form = AuthenticationForm(request, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('home')
    return render(request, 'accounts/login.html', {'form': form})

def logout_fbv(request: HttpRequest):
    if request.method == 'POST':
        logout(request)
    return logout_then_login(request)


class RegisterView(UserPassesTestMixin, CreateView):
    form_class = CustomUserCreationForm
    model = UserModel
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        return not self.request.user.is_authenticated
class ProfileDetailView(TemplateView):
    template_name = 'accounts/profile_details.html'

@login_required
@permission_required('auth.can_set_unusable_password')
def set_unusable_password(request: HttpRequest) -> HttpResponse:
    form = SetUnusablePasswordForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        selected_user = form.cleaned_data['user']
        if selected_user.is_superuser:
            messages.error(
                request,
                f"Cannot disable password for {selected_user.get_username()}"
            )
        selected_user.set_unusable_password()
        selected_user.save(update_fields=['password'])
        messages.success(
            request,
            f"Password disabled for {selected_user.get_username()}"
        )
        return redirect('home')
    return render(request, 'accounts/set_unusable_password.html', {'form': form})
