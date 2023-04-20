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

from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from django.conf import settings
from django.core.mail import send_mail

sub = "Welcome to django "
msg = 'Please verify your account'


class HomepageView(View):
    def get(self,request):
        # return render(request, 'accounts/login.html')
        return render(request, 'accounts_app/home.html')

def get_activation_link(user):
    
    """this function will return unique email activation link """
    
    # first we generating unique uid
    uid = urlsafe_base64_encode(force_bytes(user.id))
    
    # making token for user
    token = PasswordResetTokenGenerator().make_token(user=user)
    
    # activation link
    reset_link = 'http://localhost:8000/accounts/activate/confirm/'+uid+'/'+token+'/'
    
    return reset_link

def send_mail_user():
    pass

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
                user.is_active = False
                user.save()
                
                activation_link = get_activation_link(user=user)
                print('\n \n \n ')
                print(activation_link)
                
                messages.success(request, f'Congrats {uname} Your Account Successfuly Created! and Please activate to continue login')
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
            if user: # user exist 
                if not user.is_active:
                    messages.warning(request, 'Please activate your account for continue login')
                    return render(request, 'accounts/login.html')
                    
                else:
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
        
