from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from .models import *

@login_required
def Home(request):
    return render(request, 'user.html')

def about(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Send an email
        subject = 'Contact Form Submission'
        message = f'Name: {name}\nEmail: {email}\nMessage: {message}'
        # send_mail(subject, message, settings.EMAIL_HOST_USER,[email])

        email_message = EmailMessage(
                subject, message,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER]
            )

        email_message.fail_silently = True
        email_message.send()

        # Redirect to a thank you page or display a success message
        return render(request, 'thanks.html')

    return render(request, 'about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Send an email
        subject = 'Contact Form Submission'
        message = f'Name: {name}\nEmail: {email}\nMessage: {message}'
        # send_mail(subject, message, settings.EMAIL_HOST_USER,[email])

        email_message = EmailMessage(
                subject, message,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER]
            )

        email_message.fail_silently = True
        email_message.send()

        # Redirect to a thank you page or display a success message
        return render(request, 'thanks.html')

    return render(request, 'contact.html')

def RegisterView(request):

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_data_has_error = False

        if User.objects.filter(username=username).exists():
            user_data_has_error = True
            messages.error(request, 'Username already exists')
        
        if User.objects.filter(email=email).exists():
            user_data_has_error = True
            messages.error(request, 'Email already exists')

        if len(password) < 5:
            user_data_has_error = True
            messages.error(request, 'Password must be at least 5 characters')

        if not user_data_has_error:
            new_user = User.objects.create_user(
                first_name = first_name,
                last_name = last_name,
                email = email,
                username = username,
                password = password
            )
            messages.success(request, 'Account created. Login now')
            return redirect('loginview')
        else:
            return redirect('register')

    return render(request, 'register.html')

def LoginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request=request, username=username, password=password)
        if user is not None:
            # login user if login credentials are correct
            login(request, user)

            # return redirect('home')
            return redirect('user')
        else:
            # redirect back to the login page if credentials are wrong
            messages.error(request, 'Invalid username or password')
            return redirect('login')

    return render(request, 'login.html')

def LogoutView(request):

    logout(request)

    # redirect to login page after logout
    return redirect('loginview')


def ForgotPassword(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)

            # create a new reset id
            new_password_reset = PasswordReset(user=user)
            new_password_reset.save()

            # creat password reset ur;
            password_reset_url = reverse('reset-password', kwargs={'reset_id': new_password_reset.reset_id})
            full_password_reset_url = f'{request.scheme}://{request.get_host()}{password_reset_url}'

            # email content
            email_body = f'Reset your password using the link below:\n\n\n{full_password_reset_url}'

            email_message = EmailMessage(
                'Reset your password', # email subject
                email_body,
                settings.EMAIL_HOST_USER, # email sender
                [email] # email  receiver 
            )

            email_message.fail_silently = True
            email_message.send()

            return redirect('password-reset-sent', reset_id=new_password_reset.reset_id)

        except User.DoesNotExist:
            messages.error(request, f"No user with email '{email}' found")
            return redirect('forgot-password')

    return render(request, 'forgot_password.html')


def PasswordResetSent(request, reset_id):
    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return render(request, 'password_reset_sent.html')
    else:
        # redirect to forgot password page if code does not exist
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')

    return render(request, 'password_reset_sent.html')

def ResetPassword(request, reset_id):
    try:
        password_reset_id = PasswordReset.objects.get(reset_id=reset_id)

        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            passwords_have_error = False

            if password != confirm_password:
                passwords_have_error = True
                messages.error(request, 'Passwords do not match')

            if len(password) < 5:
                passwords_have_error = True
                messages.error(request, 'Password must be at least 5 characters long')

            # check to make sure link has not expired
            expiration_time = password_reset_id.created_when + timezone.timedelta(minutes=10)

            if timezone.now() > expiration_time:
                passwords_have_error = True
                messages.error(request, 'Reset link has expired')
                # delete reset id after use
                password_reset_id.delete()

            if not passwords_have_error:
                user = password_reset_id.user
                user.set_password(password)
                user.save()
            
                # delete reset id after use
                password_reset_id.delete()

                # redirect to login
                messages.success(request, 'Password reset. Proceed to login')
                return redirect('loginview')

            else:
                # redirect back to password reset page and display errors
                return redirect('reset-password', reset_id=reset_id)

    except PasswordReset.DoesNotExist:
        
        # redirect to forgot password page if code does not exist
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')
    
    return render(request, 'reset_password.html')