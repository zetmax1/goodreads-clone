from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import CustomUser
from django.shortcuts import render, redirect
from django.views import View
from users.forms import UserCreateForm, UserUpdateForm

class RegisterView(View):

    def get(self, request):
        user_form = UserCreateForm()
        context = {
            'form': user_form
        }

        return render(request, 'users/register.html', context=context)


    def post(self, request):
        context_form = UserCreateForm(data=request.POST)
        if context_form.is_valid():
            context_form.save()

            return redirect('users:login')
        else:
            context = {
                'form': context_form,
            }

            return render(request, 'users/register.html', context= context)



class LoginView(View):

    def get(self, request):
        login_form = AuthenticationForm()

        return render(request, 'users/login.html', {'login_form': login_form})

    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)

        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)

            messages.success(request, "you successfully logged in")

            return redirect('books:list')

        else:
            return render(request, 'users/login.html', {'login_form': login_form})


class ProfileView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'users/profile.html', {'user': request.user})


class LogoutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        messages.info(request, "you successfully logged out")
        return redirect('landing_page')


class UserUpdateView(LoginRequiredMixin, View):

    def get(self, request):
        user_form = UserUpdateForm(instance=request.user)
        return render(request, 'users/profile_edit.html', {'form': user_form})

    def post(self, request):
        user_form = UserUpdateForm(instance=request.user, data=request.POST, files=request.FILES,)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'You have successfully updated your profile')
            return redirect('users:profile')

        messages.error(request, 'Please enter valid information')
        return render(request, 'users/profile_edit.html', {'form': user_form})