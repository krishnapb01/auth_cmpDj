from .views import *
from django.urls import path
from django.contrib.auth import views as auth_view
from .forms import MyPasswordResetForm,MySetPasswordForm

urlpatterns = [
    path('', HomepageView.as_view(), name='homepage'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/',  LoginView.as_view(), name='login'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # change password view
    path('change-password/', PasswordChangeView.as_view(), name='change_password'),

    #logout view
    path('logout/', LogoutView.as_view(), name='logout'),


    # password reset views here
    path('reset-password/',  auth_view.PasswordResetView.as_view(template_name = 'accounts/common/reset_form.html',form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name = 'accounts/common/password_reset_done.html'), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name ='accounts/common/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-changed/succcessfuly/', auth_view.PasswordResetCompleteView.as_view(template_name = 'accounts/common/password_reset_complete.html'), name='password_reset_complete'),
    
    path('update-profile/', UpdateProfileView.as_view(), name='update_profile'),
    path('add-address/', AddAddress.as_view(), name='add_address'),


    
    

   
]
