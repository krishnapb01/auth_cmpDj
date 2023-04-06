from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth.models import User

from django import forms
from .models import Profile, Address

class AddressForm(forms.ModelForm):
    class Meta:
        model  = Address
        fields = ('name', 'city', 'state', 'pincode')

        widgets = {
            'state':forms.Select(attrs={'class': 'form-control', 'placeholder': 'State'}),

            'name':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Name here'}),
            'city':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter City here'}),
            'pincode':forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Pincode here'}),
            
        }



# User Signup form
class SignupForm(UserCreationForm):
    """User Signup Form: fields are username, first_name, last_name, email and password"""
    password1 =  forms.CharField(label='Password',error_messages={'required': 'Password  is required'}, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Enter Password her..'}))
    password2 =  forms.CharField(label='Confirm Password',error_messages={'required': 'Confirm passsword  is required'}, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Enter Password her..'}))
    email     =  forms.CharField(required=True,error_messages={'required': 'Email id is required'},  widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter  Email id here ..'}))
    first_name=  forms.CharField(required=True,error_messages={'required': 'First name is required'}, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name here ..'} ))
    last_name =  forms.CharField(required=True,error_messages={'required': 'Last name  is required'}, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name here ..'} ))

    

    class Meta:
        model  = User
        fields = ('username', 'email', 'first_name', 'last_name')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username here ..'})
        }

        error_messages = {
            'username': {'required': 'Username is required!'}
        }

# User Login or Authentication form
class LoginForm(AuthenticationForm):
    """User Authentication Form fields: username and password only"""
    username = forms.CharField(error_messages={'required': 'Username is reuired!'}, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username here..'}))
    password = forms.CharField(error_messages={'required': 'Password is required!'}, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password here'}))

# User Password Change form
class ChangePassword(PasswordChangeForm):
    """ Password Change Form using existing password(old password) and with new_password1 and new_password2 """

    old_password =  forms.CharField(error_messages={'required': 'Your Old Password is required!'}, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Your Old Password here..'}))
    new_password1  =  forms.CharField(error_messages={'required': 'Please Enter New Password!'}, label='New Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Your New Password here..'}))
    new_password2 =  forms.CharField(error_messages={'required': 'Confirm Password is required!'}, label='Confirm Password(again)', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password here..'}))


# password reset form here
class MyPasswordResetForm(PasswordResetForm):
    """This is Password Reset Form for reseting means it take email only of register user and make query to database further operation."""
    email = forms.CharField(error_messages={'required': 'Email is required!'}, widget=forms.EmailInput(attrs={'class': 'form-control','autocomplete': 'email',  'placeholder': 'Enter attached email id with your account'}))

# set password form 
class MySetPasswordForm(SetPasswordForm):
    """Set Password Form. This will diplay  form to set new password  fields new_password1 and new_password2"""

    new_password1  = forms.CharField(label='New Password', error_messages={'required': 'New password is required'}, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter new password ..',}))
    new_password2  = forms.CharField(label='Confirm New Password', error_messages={'required': 'Confirm password is required'}, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm  new password ..'}))


class UserProfileForm(forms.ModelForm):
    """User Profile Form to update users profiles contains: user_pic, bio and address only"""

    class Meta:
        model  = Profile
        fields = ('pic', 'bio', 'address')

        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tell abouts your self'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your address here'})
        }