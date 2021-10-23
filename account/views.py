from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserCreationForm, UserSignInForm, UserChangeForm
from .models import *
from blog.models import Article, AboutArticle
from club.models import Event
from youtube.models import Youtube
from pytz import timezone
from datetime import datetime

def home(request):
    user = None
    if request.user.is_authenticated:
        user = request.user
    article = Article.objects.filter(aboutarticle__isnull=True).last()
    asia = timezone('Asia/Taipei')
    club = Event.objects.filter(start_time__gte=datetime.now().astimezone(asia)).order_by('start_time').first()
    video = Youtube.objects.last()
    return render(request, 'account/home.html', {
        'user': user,
        'article': article,
        'club': club,
        'video': video,
    })

def signup(request):
    create_form = UserCreationForm()
    signup = True
    if request.method == 'POST':
        create_form = UserCreationForm(request.POST)
        if create_form.is_valid():
            user = SiteUser.objects.create_user(
                email=create_form.cleaned_data['email'].lower(),
                first_name=create_form.cleaned_data['first_name'],
                last_name=create_form.cleaned_data['last_name'],
                date_of_birth=create_form.cleaned_data['date_of_birth'],
                password=create_form.cleaned_data['password1'],
            )
            login(request, user)
            return redirect('/')
        else:
            return render(request, "account/signup.html", {'create_form': create_form, 'signup': signup,})
    return render(request, 'account/signup.html', {'create_form': create_form, 'signup': signup,})

def signin(request):
    signin_form = UserSignInForm()
    errors = None
    error_link = None
    if request.POST:
        signin_form = UserSignInForm(request.POST)
        redirect_url = request.POST.get('next', None)
        if signin_form.is_valid():
            user = authenticate(email=signin_form.cleaned_data['email'].lower(), password=signin_form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                if redirect_url:
                    return redirect(redirect_url)
                else:
                    return redirect('/')
            else:
                email = signin_form.cleaned_data['email'].lower()
                user = SiteUser.objects.filter(email=email).first()
                if user:
                    errors = 'Login Failed - Incorrect Password.'
                    error_link = {'msg': 'Reset Password', 'link': '/#'}
                    return render(request, 'account/signin.html', {
                        'signin_form': signin_form,
                        'errors': errors,
                        'error_link': error_link,
                    })
                else:
                    errors = 'Login Failed - Email does not exist.'
                    error_link = {'msg': 'Register Now', 'link': '/signup'}
                    return render(request, 'account/signin.html', {
                        'signin_form': signin_form,
                        'errors': errors,
                        'error_link': error_link,
                    })

        else:
            errors = 'Login Failed - Please try again.'
            return render(request, 'account/signin.html', {'signin_form': signin_form, 'errors': errors,})
    return render(request, 'account/signin.html', {
        'signin_form': signin_form,
        'errors': errors,
        'error_link': error_link,
    })

@login_required
def signout(request):
    logout(request)
    return redirect('/')

@login_required
def settings(request):
    user = request.user
    create_form = UserChangeForm(instance=user)
    signup = False
    if request.method == 'POST':
        create_form = UserChangeForm(request.POST)
        if create_form.is_valid():
            user.first_name=create_form.cleaned_data['first_name']
            user.last_name=create_form.cleaned_data['last_name']
            user.date_of_birth=create_form.cleaned_data['date_of_birth']
            user.set_password(create_form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('/')
        else:
            return render(request, "account/signup.html", {'create_form': create_form})
    return render(request, 'account/signup.html', {
        'create_form': create_form,
        'signup': signup,
        'user': user,
    })

def about(request):
    about_page_content = AboutArticle.objects.last().content if AboutArticle.objects.last() else None
    return render(request, 'account/about.html', {
        'about_page_content': about_page_content,
    })
