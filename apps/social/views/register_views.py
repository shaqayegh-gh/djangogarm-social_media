from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.base import View
from .common_views import get_random_otp, send_otp
from apps.social.forms import RegisterFrom, LoginForm
from apps.social.models import User, Profile


def djangogram_redirect(request):
    return redirect('/djangogram/')


def login_redirct(request):
    return redirect('user_login')


class SignUpView(View):
    """signup view for register a new user"""

    def get(self, request):
        if request.user.is_authenticated:  # redirect to homepage if the user is authenticated yet
            return redirect('home')
        else:
            signup_form = RegisterFrom()
            return render(request, 'registration/register-user.html', {'signup_form': signup_form})

    def post(self, request):
        signup_form = RegisterFrom(request.POST)
        if signup_form.is_valid():
            user = signup_form.save(commit=False)
            request.session['phone_number'] = user.phone_number
            # send otp
            otp = get_random_otp()
            # send_otp(user.phone_number, otp)
            # save otp
            user.otp = otp
            user.is_active = False
            print(user.otp)
            user.save()
            Profile.create_user_profile(user=User.objects.get(username=request.POST.get('username')))
            return HttpResponseRedirect(reverse('sms_verify'))

        else:
            print(signup_form.error_messages)
            message = signup_form.errors
            return render(request, 'registration/register-user.html',
                          {'signup_form': RegisterFrom(), 'message': message})


def sms_verify(request):
    if request.method == "GET":
        phone_number = request.session.get('phone_number')
        return render(request, 'registration/sms_verify.html', {"phone_number": phone_number})

    if request.method == 'POST':
        try:
            phone_number = request.session.get('phone_number')
            print(phone_number)
            user = User.objects.get(phone_number=phone_number)
            if user.otp != int(request.POST.get('otp')):
                print("wrong")
                return render(request, 'registration/sms_verify.html', {"message": "Wrong code. Enter correct code."})
            else:
                user.is_active = True
                user.save()
                print("active saved")
                login(request, user)
                request.session['user_id'] = user.id.hex  # make a session by user.id
                user.is_online = True  # make online status for user after login
                user.save()
                return redirect('home')
                # return redirect('user_login')
        except:
            return HttpResponseRedirect(reverse('signup'))


def login_user(request):
    if request.user.is_authenticated:  # redirect to homepage if the user is authenticated
        return redirect('home')
    else:
        if request.method == 'GET':
            login_form = LoginForm()
            return render(request, 'registration/login.html', {'form': login_form})

        if request.method == 'POST':
            input_username = request.POST.get('username')
            input_password = request.POST.get('password')
            user = authenticate(request, username=input_username, password=input_password)
            if user:
                if user.is_active:  # check the user active status
                    login(request, user)
                    request.session['user_id'] = user.id.hex  # make a session by user.id
                    user = User.objects.get(pk=request.session.get('user_id'))
                    user.is_online = True  # make online status for user after login
                    user.save()
                    return redirect('home')
                else:
                    message = 'your account is not active. make a new account.'
            else:
                message = 'username or password not correct'
            return render(request, 'registration/login.html', {"form": LoginForm(), 'message': message})
        context = {"form": LoginForm()}
        return render(request, 'registration/login.html', context)


def logout_user(request):
    try:
        user = User.objects.get(pk=request.session.get('user_id'))
        user.is_online = False  # make offline status after logging out
        user.save()
        del request.session['user_id']  # delete the user session after logging out
    except:
        pass
    logout(request)
    return redirect('user_login')  # redirect to login page after logging out
