from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import CreateUserForm
from .models import *
from django.contrib import messages


# Create your views here.
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        # print(form.subscribe_to)

        if form.is_valid():
            subscribe_to = form.cleaned_data.get("subscribe_to")
            user_obj = form.save()
            user = form.cleaned_data.get('username')
            for each in subscribe_to:
                obj = NewsCategory.objects.get(pk=each)
                obj.subscribers.add(user_obj)
            messages.success(request, 'Account was created for ' + user)

            return JsonResponse({'error': False, 'message': 'User Added Successfully'})
        else:
            print(form.errors)
            return JsonResponse({'error': True, 'errors': form.errors})

    context = {'form': form, 'edit': False}
    return render(request, 'newsfilter/register.html', context=context)


# @login_required(login_url='login')
# def list_users(request):
#     users = User.objects.all()
#     context = {"users": users}
#     return render(request, 'users/list_users.html', context=context)


@login_required(login_url='login')
def overview(request):
    news = NewsRecord.objects.all()

    context = {
        "news": news
    }

    return render(request, 'newsfilter/news_overview.html', context=context)


@login_required(login_url='login')
def authenticate_news(request, id):
    news = NewsRecord.objects.get(pk=id)

    if request.method == "POST":
        print(request.POST)
        if request.POST.get("yes"):
            news.authentic_count += 1
        else:
            news.fake_count += 1
        news.save()

        return redirect('thankyou')

    context = {
        "news": news
    }

    return render(request, 'newsfilter/authenticate_news.html', context=context)


@login_required(login_url='login')
def news_detail(request, id):
    news = NewsRecord.objects.get(pk=id)
    print(news)

    context = {
        "news": news
    }

    return render(request, 'newsfilter/news_detail.html', context=context)


def thankyou(request):
    return render(request, 'newsfilter/thankyou.html')


def log_in_user(request):
    if request.user.is_authenticated:
        return redirect('news_overview')
    else:
        if request.method == 'POST':
            username = request.POST.get('unm')
            password = request.POST.get('pwd')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('news_overview')
            else:
                messages.info(request, 'Username OR password is incorrect')

    return render(request, 'newsfilter/login.html')


@login_required(login_url='login')
def log_out_user(request):
    logout(request)
    return redirect('login')
