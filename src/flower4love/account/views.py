from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import JsonResponse, Http404
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.db import transaction

from account.models import UserProfile
from account.forms import RegistertForm, LoginForm, PasswordFindForm, modifypasswordForm, PasswordResetForm
from common.utils import send_mail

import logging
logger = logging.getLogger(__name__)


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            user = authenticate(**form_data)

            if not user:
                return render(request, 'account/login.html', {
                    'res': 'error',
                    'message': 'login failed',
                    'form': form
                })

            auth.login(request, user)

            if not request.POST.get('remember_me', None):
                request.session.set_expiry(0)

            if request.GET.get('next'):
                return HttpResponseRedirect(request.GET.get('next'))
            return HttpResponseRedirect('/')

    form = LoginForm()
    return render(request, 'account/login.html', {
        'message': 'login failed',
        'form': form
    })


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/account/login')


def check_username_duplicate(request):
    if User.objects.filter(username=request.GET.get('username')):
        # username has been registered
        return JsonResponse({'res': 'error'})
    return JsonResponse({'res': 'ok'})


@transaction.atomic
def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        form = RegistertForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            if not User.objects.filter(username=form_data['username']):

                user = User()
                user.username = form_data['username']
                user.email = form_data['email']
                user.set_password(form_data['password1'])
                user.save()

                user_profile = UserProfile()
                user_profile.user_id = user.id
                user_profile.save()

                return HttpResponseRedirect('/account/login')

    form = RegistertForm()
    return render(request, 'account/register.html',{
        'form': form
    })


def password_find(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        email = request.POST.get('email')
        user_exist = User.objects.filter(email=email)
        if user_exist:
            site = 'http://%s' % request.get_host()
            # send mail
            user = user_exist[0]
            token = default_token_generator.make_token(user)
            to_mail_list = [email]
            subject = 'Reset Password'
            body = site + '/account/reset_psd/%s/%s/' % (user.id, token)
            send_mail(to_mail_list, subject, body)

            return render(request, "account/find_psd_success.html",{})

    form = PasswordFindForm()
    return render(request, "account/find_psd.html",{
        'form': form
    })


def reset_password(request, uidb64=None, token=None):
    user_id = uidb64
    user_set = User.objects.filter(id=user_id)
    if not (uidb64 and token and user_set):
        raise Http404

    user = user_set[0]
    user_token_check_result = default_token_generator.check_token(user, token)
    if not user_token_check_result:
        raise Http404

    if request.method == 'GET':
        return render(request, "account/reset_password.html",
                      {'form': PasswordResetForm},
                      )
    elif request.method == 'POST':
        new_password = request.POST.get('new_password')
        user.set_password(new_password)
        user.save()
        return render(request, "account/reset_password_success.html", {
        })

@login_required
def modify_password(request):
    if request.method == 'POST':
        form = modifypasswordForm(request.POST)
        if form.is_valid():
            form_info = form.cleaned_data
            username = request.user.username
            oldpassword = form_info['old_password']
            user = auth.authenticate(username=username, password=oldpassword)
            if user is not None and user.is_active:
                newpassword = form_info['password1']
                user.set_password(newpassword)
                user.save()
                user = authenticate(username=username, password=newpassword)
                auth.login(request, user)
                return HttpResponseRedirect("/account/center/index")
    else:
        form = modifypasswordForm()
    return render(request, 'account/modifypassword.html', {
        'form': form
    })


# ----------------- request context -------------
def user_profile(request):
    user_id = request.user.id
    if user_id:
        user_profile_data = UserProfile.objects.get(user_id=user_id)
        return {'user_profile': user_profile_data}
    return {}
