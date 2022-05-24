from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from article.models import Article
from discussion.models import Discussion
from like.models import ArticleLike, DiscussionLike


@login_required(login_url='/account/login')
@csrf_exempt
def post_article_like(request):
    user = request.user
    article_id = request.POST.get('article_id')
    like_type = request.POST.get('type')
    status = request.POST.get('status')
    if like_type == 'article':
        article = Article.objects.filter(id=article_id)[0]
        like, created = ArticleLike.objects.get_or_create(user=user, article=article)

    if status == 'true':
        like.status = True
        article.like_count += 1
    else:
        like.status = False
        article.like_count -= 1
    like.save()
    article.save()
    data = {
        'like_count': article.like_count,
        'status': like.status,
    }
    return JsonResponse(data, content_type='application/json', safe=False)


@login_required(login_url='/account/login')
@csrf_exempt
def post_discussion_like(request):
    user = request.user
    discussion_id = request.POST.get('discussion_id')
    like_type = request.POST.get('type')
    status = request.POST.get('status')
    if like_type == 'discussion':
        discussion = Discussion.objects.filter(id=discussion_id)[0]
        like, created = DiscussionLike.objects.get_or_create(user=user, discussion=discussion)

    if status == 'true':
        like.status = True
        discussion.like_count += 1
    else:
        like.status = False
        discussion.like_count -= 1
    like.save()
    discussion.save()
    data = {
        'like_count': discussion.like_count,
        'status': like.status,
    }
    return JsonResponse(data, content_type='application/json', safe=False)


