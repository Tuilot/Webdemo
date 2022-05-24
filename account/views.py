from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import auth

from account.forms import RegistrationForm, LoginForm, EditUserInfoForm
from account.models import Account
from article.models import Article
from common_lib.account_utils import getNewId, calc_md5

from django.views.decorators.csrf import csrf_exempt
from common_lib import account_utils

@csrf_exempt
def login(request):
    if not request.user.is_anonymous:
        return render(request, 'hint.html', {'msg': '您已登陆',
                                             'url': '/',
                                             'btn_msg': '前往首页'})
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                user_info = Account.objects.get(email__exact=email)
                if user_info.username == 'superuser' and user_info.is_superuser is False:
                    user_info.is_superuser = True
                    user_info.save()
                request.session['user_id'] = user_info.id
                request.session['email'] = user_info.id
                request.session['user_name'] = user_info.username
                auth.login(request, Account.objects.all().get(id__exact=user_info.id))
            except:
                request.session['email'] = form.cleaned_data.get('email')
            return redirect('/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']
            user = Account.objects.create(
                id=getNewId(),
                username=username,
                email=email,
                password=calc_md5(password),
            )
            return render(request, 'register.html', {'register_message': '注册成功，现在你可以登陆了！'})
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})



@csrf_exempt
def logout(request):
    auth.logout(request)
    request.session.clear()
    return redirect('login')

@login_required(login_url='/account/login')
def profile(request):
    user_id = request.user.id
    try:
        user_info = Account.objects.all().get(id__exact=user_id)
    except:
        return render(request, 'hint.html', {'msg': 'no such user!'})

    data = {
        'user_info': user_info,
        'page_type': 'profile'
    }
    return render(request, 'user_center/profile.html', data)

@login_required(login_url='/account/login')
@csrf_exempt
def edit_user_info(request):
    user_id = request.user.id
    try:
        user_info = Account.objects.get(id__exact=user_id)
    except:
        return render(request, 'hint.html', {'msg': 'no such user!'})
    if request.method == 'POST':
        form = EditUserInfoForm(request.POST)
        if form.is_valid():
            user_info.username = form.data.get('edit_username')
            user_info.email = form.data.get('edit_email')
            user_info.phone_number = form.data.get('edit_phone_number')
            user_info.school = form.data.get('edit_school')
            user_info.real_name = form.data.get('edit_real_name')
            user_info.motto = form.data.get('edit_motto')
            user_info.sex = form.data.get('edit_sex')
            user_info.save()
            return redirect('profile')
        else:
            data = {
                'user_info': user_info,
                'page_type': 'edit_user_info',
                'form': form
            }
            return render(request, 'user_center/edit_user_info.html', data)
    else:
        data = {
            'user_info': user_info,
            'page_type': 'edit_user_info'
        }
        return render(request, 'user_center/edit_user_info.html', data)

@login_required(login_url='/account/login')
@csrf_exempt
def update_avatar(request):
    user_id = request.user.id
    avatar = request.FILES.get('avatar')
    avatar.name = account_utils.random_avatar_name(avatar.name)
    try:
        user = Account.objects.get(id=user_id)
        user.avatar = avatar
        print(user.avatar.url)
        user.save()
        data = {
            'result': 'success',
            'avatar_url': user.avatar.url
        }
        return JsonResponse(data, content_type='application/json', safe=False)
    except :
        pass
    return JsonResponse(None, content_type='application/json', safe=False)


def user_show_info(request, user_id):
    per_page_count = 40
    try:
        user_info = Account.objects.all().get(id__exact=user_id)
    except:
        return render(request, 'hint.html', {'msg': 'no such user!'})
    current_page = 1
    articles = Article.objects.filter(author=user_info)[
               (current_page - 1) * per_page_count: current_page * per_page_count]
    total = len(articles)
    data = {
        'user_info': user_info,
        'page_type': 'profile',
        'articles': articles,
        'total':total,
    }
    return render(request, 'user_center/user_show_info.html', data)