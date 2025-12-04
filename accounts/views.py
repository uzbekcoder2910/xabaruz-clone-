from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from .forms import LoginForm, UserRegisterForm, UserEditForm, ProfileEditForm
from .models import Profile


# Create your views here.
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            user = authenticate(request,username=data['username'], password=data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('success')
                else:
                    return HttpResponse('error(your profile is not active)')
            else:
                return HttpResponse('error(username or password incorrect)')
    else:
        form = LoginForm()
        context = {'form': form}
    return render(request, 'registration/login.html', context=context)

def logout_view(request):
    logout(request)
    return render(template_name='registration/logged_out.html', request=request)
@login_required
def dashboard_view(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    context = {'user': user, 'profile': profile}
    return render(request, 'pages/user_profile.html', context=context)

def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # User yaratilganda bo'sh profil ham qo'shib qoyadi. keyin biz Edit yordamida unga malumotlar kiritamiz.
            Profile.objects.create(user=user)
            context = {'user': user}
            return render(request, 'pages/register_done.html', context=context)
        else:
            return redirect('signup/')
    else:
        form = UserRegisterForm()
        context = {'form': form}
        return render(request, 'pages/register.html', context=context)

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'pages/register.html'
@login_required
def edit_user(request):
    if request.method == 'POST':
        form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
    else:
        form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'pages/profile_edit.html', {'form': form, 'profile_form': profile_form})

class EditUserView(LoginRequiredMixin, View):
    def get(self, request):
        form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request, 'pages/profile_edit.html', {'form': form, 'profile_form': profile_form})

    def post(self, request):
        form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('user_profile')
