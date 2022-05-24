from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from account.models import Account
from article.models import Article
from common_lib.tool_utils import get_pagination
from discussion.models import Discussion
from resource.models import FileResource


def article_manager(request):
    article_list = Article.objects.filter()
    article_len = len(article_list)
    page = request.GET.get('page', default=1)
    page = int(page)
    pagination = get_pagination(page, (article_len + 14) // 15)
    data = {
        'article_list': article_list,
        'pagination': pagination
    }
    return render(request, 'article_manager.html', data)


@csrf_exempt
@login_required(login_url='/account/login')
def delete_article(request):
    user = request.user
    article_id = request.POST.get('article_id')
    try:
        article = Article.objects.filter(id=article_id).first()
        article.delete()
    except Exception as e:
        print(e)
        pass
    return JsonResponse(None, content_type='application/json', safe=False)


def resource_manager(request):
    page = request.GET.get('page', default=1)
    page = int(page)
    resource_list = FileResource.objects.filter()
    resource_len = len(resource_list)
    pagination = get_pagination(page, (resource_len + 14) // 15)
    data = {
        'resource_list': resource_list,
        'pagination': pagination,
    }
    return render(request, 'resource_manager.html', data)


@csrf_exempt
def delete_resource(request):
    user = request.user
    resource_id = request.POST.get('resource_id')
    try:
        article = FileResource.objects.filter(id=resource_id).first()
        article.delete()
    except:
        pass
    return JsonResponse(None, content_type='application/json', safe=False)


def account_manager(request):
    page = request.GET.get('page', default=1)
    page = int(page)
    account_list = Account.objects.filter()
    account_len = len(account_list)
    pagination = get_pagination(page, (account_len + 14) // 15)
    data = {
        'account_list': account_list,
        'pagination': pagination,
    }
    return render(request, 'account_manager.html', data)


def discussion_manager(request):
    discussion_list = Article.objects.filter()
    discussion_len = len(discussion_list)
    page = request.GET.get('page', default=1)
    page = int(page)
    pagination = get_pagination(page, (discussion_len + 14) // 15)
    data = {
        'discussion_list': discussion_list,
        'pagination': pagination
    }
    return render(request, 'discussion_manager.html', data)


@csrf_exempt
@login_required(login_url='/account/login')
def delete_discussion(request):
    user = request.user
    discussion_id = request.POST.get('discussion_id')
    try:
        discussion = Discussion.objects.filter(id=discussion_id).first()
        discussion.delete()
    except :
        pass
    return JsonResponse(None, content_type='application/json', safe=False)