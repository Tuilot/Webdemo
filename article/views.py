import datetime
import re

import markdown
from django.views.decorators.csrf import csrf_exempt

from article.models import Article
# Create your views here.
from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from mdeditor.fields import MDTextFormField

from comment.forms import CommentForm
from comment.views import get_article_comment
from common_lib.article_utils import create_article_id

import markdown2

# from comments.forms import CommentForm
# from comments.get_comment_tree import get_comment_tree
from common_lib.tool_utils import get_pagination
from like.models import ArticleLike

from datetime import datetime, timezone


def article_list(request):
    try:
        keyword = request.POST.get('keyword', default='')
        art_type = request.GET.get('type', default='c')
        page = request.GET.get('page', default=1)
        page = int(page)
        order_by = request.GET.get('order_by', default='release_time')
        # if order_by == 'view_count' or order_by == 'like_count' or order_by == 'comment_count' or :
        order_by = '-' + order_by
        articles_list = Article.objects.filter(title__contains=keyword, type=art_type).order_by(order_by)[(page - 1) * 20: page * 20]
        user = request.user
        article_count = Article.objects.count()
        page_count = (article_count + 19) // 20
        pagination = get_pagination(page, page_count)
        data = {
            'articles': articles_list,
            'total': len(articles_list),
            'choice_file_type': Article.ChoiceFileType,
            'file_type': art_type,
            'pagination': pagination,
            'order_by': order_by,
        }
        return render(request, 'article_list.html', data)
    except Exception as e:
        return render(request, '404_page.html', {'error_msg': e,
                                                 'btn_msg': '返回首页'})


def change_formula(matched):
    formula = matched.group(0)
    formula = formula.replace('_', ' _')
    return '\n<p>' + formula + '</p>\n'


def query_is_like(article_id, user):
    if user.is_anonymous:
        return False
    article = Article.objects.filter(id=article_id)[0]
    if ArticleLike.objects.filter(article=article, user=user).exists():
        is_like = ArticleLike.objects.filter(article=article, user=user)[0].status
        return is_like
    else:
        return False


def article_detail(request, article_id):
    try:
        article = Article.objects.all().get(id__exact=article_id)
    except:
        return render(request, 'article_detail.html', {'msg': 'article not found!'})
    if request.user.id != article.author.id:
        article.view_count += 1
    article.save()
    # article.content = markdown2.markdown(re.sub(r'\$\$(.+?)\$\$', change_formula, article.content))
    article.content = markdown.markdown(article.content, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    is_like = query_is_like(article.id, request.user)
    # is_favorite = query_is_favorite(article.id, request.user)
    form = CommentForm()
    comment_list = get_article_comment(article)
    data = {
        'article': article,
        'is_like': is_like,
        # 'is_favorite': is_favorite,
        'author_id': article.author.id,
        'comment_list': comment_list,
        'form': form
    }
    return render(request, 'article_detail.html', data)


class BlogForm(forms.Form):
    content = MDTextFormField(label='')


@method_decorator(login_required(login_url='/account/login'), name='dispatch')
class Edit(View):
    def get(self, request):
        form = BlogForm()
        data = {
            'form': form,
            'choice_file_type': Article.ChoiceFileType,
        }
        return render(request, 'articles_edit.html', data)

    def post(self, request):
        title = request.POST.get('title')
        file_type = request.POST.get('file_type')
        content = request.POST.get('content')
        article_id = create_article_id()
        author = request.user
        Article.objects.create(id=article_id,
                               title=title,
                               type=file_type,
                               author=author,
                               content=content)
        data = {
            'msg': '发布成功！',
            'url': '/article/' + article_id,
            'btn_msg': '前往查看文章'
        }
        return render(request, 'hint.html', data)


def get_hot_num(article):
    num = 0
    day = (datetime.now(timezone.utc) - article.release_time).days + 1
    return (article.view_count + article.like_count * 2 + article.comment_count * 3 +
            article.favorite_count * 4 + 10) / (day * day)


def get_hot_list():
    articles = Article.objects.all()
    nums = []
    for article in articles:
        nums.append((-get_hot_num(article), article.id))
    nums.sort()
    nums = nums[0:10]
    hot_list = []
    for num in nums:
        hot_list.append(Article.objects.all().get(id=num[1]))
    return hot_list


@login_required(login_url='/account/login')
def front_page(request):
    hot_list = get_hot_list()
    latest_list = Article.objects.all().order_by('-release_time')[0:10]
    data = {
        'hot_list': hot_list,
        'latest_list': latest_list,
    }
    return render(request, 'front_page.html', data)
