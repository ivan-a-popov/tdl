from django.shortcuts import render

from django.core.mail import send_mail
from django.shortcuts import redirect
from django.contrib import auth, messages

from accounts.models import Token

from django.urls import reverse

from django.contrib.auth import logout


def send_login_email(request):
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse('login') + '?token=' + str(token.uid)
    )
    message_body = f'Use this link to log in:\n\n{url}'
    send_mail(
        'Your login link for ToDoLists',
        message_body,
        'i.popov@helpist.ru',
        [email],
    )
    messages.success(
        request,
        "Please, check your email, we've sent you a link you can use to log in."
    )
    return redirect('/')

def login(request):
    user = auth.authenticate(uid=request.GET.get('token'))
    if user:
        auth.login(request, user)
    return redirect('/')

def logout_view(request):
    logout(request)
    return redirect('/')

