from django.views import View
from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail

from .forms import SignupForm,LoginForm,ChangePassword
from .forms import UserProfileForm, AddressForm

from .models import Profile,Address
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


class HomepageView(View):
    def get(self,request):
        # return render(request, 'accounts/login.html')
        return render(request, 'accounts_app/home.html')

class SignupView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            form = SignupForm()
            return render(request, 'accounts/signup.html', {'form': form})
        else:
           return redirect('dashboard')
        
    def post(self, request):
        if not request.user.is_authenticated:

            form = SignupForm(request.POST)
            if form.is_valid():
                uname = str(form.cleaned_data['username']).title()
                user = form.save()
                group  = Group.objects.get(name = 'Author')
                user.groups.add(group)
                messages.success(request, f'Congrats {uname} Your Account Successfuly Created! and Added in Author Group')
                return redirect('login')
            return render(request, 'accounts/signup.html', {'form': form})
        else:
           return redirect('dashboard')
        
class LoginView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            form =  LoginForm()
            return render(request, 'accounts/login.html',{'form': form})
        else:
            return redirect('dashboard') 
    def post(self, request):
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            uname = form.cleaned_data.get('username', None)
            password = form.cleaned_data.get('password', None)
            user = authenticate(username=uname, password=password)
            if user is not None:
               login(request, user)
               messages.success(request, f'Congrats {request.user.username} You have successfuly logged in dashboard ')
               return redirect('dashboard')
            
        return render(request, 'accounts/login.html',{'form': form})
            
class DashboardView(LoginRequiredMixin,View):
   def get(self, request):
        profile = Profile.objects.get(user__id = request.user.id)
        context = {
            'profile': profile
        }
        print(profile)
        return render(request, 'accounts/dashboard.html', context)
     
class PasswordChangeView(LoginRequiredMixin, View):
   
    def get(self, request):
           form = ChangePassword(user=request.user)
           return render(request, 'accounts/changepassword.html', {'form': form})
        
    def post(self, request):
        if request.user.is_authenticated:
            user = request.user
            form = ChangePassword(user=user, data=request.POST)
            if form.is_valid():
                form.save()
                user = str(request.user).title()
                messages.success(request, f'Congrats! {user} Your Password Changed Successfuly ')
                return redirect('dashboard')
            return render(request, 'accounts/changepassword.html', {'form': form})
        else:
            return redirect('login')
            
class LogoutView(LoginRequiredMixin, View):

    def get(self, request):
        if request.user.is_authenticated:
            user = str(request.user).title()
            logout(request)
            messages.success(request, f'{user} Your Successfuly Logout Thanks From  Krishna(admin) To Visit Our Website!  ')
            return redirect('login')
        else:
            return redirect('login')         

class UpdateProfileView(LoginRequiredMixin, View):
    def get(self, request):
        profile = Profile.objects.get(user__username = request.user.username)
        form  = UserProfileForm(instance=profile)
        return render(request, 'accounts/update_profile.html', {'form': form})  
    
    def post(self, request):
        profile  = Profile.objects.get(user__username = request.user.username)
        form  = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congrats Your Profile Successfuly Updated!')
            return redirect('dashboard')
        return render(request, 'accounts/update_profile.html', {'form': form})  
        
class AddAddress(LoginRequiredMixin, View):
    def get(self, request):
        form  = AddressForm()
        return render(request, 'accounts/add_address.html', {'form': form})  
    
    def post(self, request):
        user = request.user
        form  = AddressForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            pincode = form.cleaned_data['pincode']
            address = Address.objects.create(user=user, name=name, city=city, state = state, pincode=pincode)
            try:
                address.save()
            except:
                pass
            else:
                messages.success(request, 'Congrats! Address Added Successfuly')
                return redirect('dashboard')
        return render(request, 'accounts/add_address.html', {'form': form})  
        
