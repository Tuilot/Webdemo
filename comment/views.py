from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from account.models import Account
from article.models import Article
from comment.forms import CommentForm
from comment.models import ArticleComment, DiscussionComment
from discussion.models import Discussion


def get_comment(comments):
    fa = {}
    son = {}
    comment_list = []
    for comment in comments:
        if comment.comment_id == -1:
            fa[comment.id] = comment.id
            son[comment.id] = []
        else:
            fa[comment.id] = fa[comment.comment_id]
            son[fa[comment.id]].append(comment)
    for comment in comments:
        if comment.comment_id == -1:
            comment_list.append([comment, son[comment.id]])
    return comment_list


def get_article_comment(article):
    comments = ArticleComment.objects.filter(article=article).order_by("comment_time")
    return get_comment(comments)


def get_discussion_comment(discussion_id):
    comments = DiscussionComment.objects.filter(discussion=discussion_id)
    return get_comment(comments)


@csrf_exempt
@login_required(login_url='/account/login')
def post_article_comment(request):
    article_id = request.POST.get('article_id')
    form = CommentForm(request.POST)
    article = Article.objects.filter(id=article_id)[0]
    if form.is_valid():
        try:
            commenter = request.user
            content = form.data.get('content')
            ArticleComment.objects.create(commenter=commenter,
                                          content=content,
                                          article=article)
            article.comment_count += 1
            article.save()
        except:
            pass
    comment_list = get_article_comment(article)
    data = {
        'comment_list': comment_list,
        'article': article
    }
    return render(request, 'comment.html', data)


@csrf_exempt
@login_required(login_url='/account/login')
def post_article_reply(request):
    article_id = request.POST.get('article_id')
    comment_id = request.POST.get('comment_id')
    reply_user = ArticleComment.objects.filter(id=comment_id)[0].commenter
    comment = request.POST.get('comment')
    article = Article.objects.filter(id=article_id)[0]
    try:
        commenter = request.user
        if commenter.is_anonymous is not True:
            ArticleComment.objects.create(commenter=commenter,
                                          content=comment,
                                          article=article,
                                          comment_id=comment_id,
                                          reply_user_id=reply_user.id,
                                          reply_user_name=reply_user.username)
    except:
        pass

    comment_list = get_article_comment(article)
    data = {
        'comment_list': comment_list,
        'article': article
    }
    return render(request, 'comment.html', data)


@csrf_exempt
@login_required(login_url='/account/login')
def post_discussion_comment(request):
    discussion_id = request.POST.get('discussion_id')
    form = CommentForm(request.POST)
    discussion = Discussion.objects.filter(id=discussion_id)[0]
    if form.is_valid():
        try:
            commenter = request.user
            content = form.data.get('content')
            DiscussionComment.objects.create(commenter=commenter,
                                             content=content,
                                             discussion=discussion)
            discussion.comment_count += 1
            discussion.save()
        except:
            pass
    comment_list = get_discussion_comment(discussion)
    data = {
        'comment_list': comment_list,
        'discussion': discussion
    }
    return render(request, 'comment.html', data)


@csrf_exempt
@login_required(login_url='/account/login')
def post_discussion_reply(request):
    discussion_id = request.POST.get('discussion_id')
    comment_id = request.POST.get('comment_id')
    reply_user = DiscussionComment.objects.filter(id=comment_id)[0].commenter
    comment = request.POST.get('comment')
    discussion = Discussion.objects.filter(id=discussion_id)[0]
    try:
        commenter = request.user
        if commenter.is_anonymous is not True:
            DiscussionComment.objects.create(commenter=commenter,
                                             content=comment,
                                             discussion=discussion,
                                             comment_id=comment_id,
                                             reply_user_id=reply_user.id,
                                             reply_user_name=reply_user.username)
    except:
        pass

    comment_list = get_discussion_comment(discussion)
    data = {
        'comment_list': comment_list,
        'discussion': discussion
    }
    return render(request, 'comment.html', data)
