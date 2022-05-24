import re

import markdown
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View

from article.views import BlogForm, change_formula
from comment.forms import CommentForm
from comment.views import get_discussion_comment
from common_lib.discussion_utils import create_discussion_id
from common_lib.tool_utils import get_pagination
from discussion.models import Discussion
from like.models import DiscussionLike


def discussion_list(request):
    try:
        keyword = request.POST.get('keyword', default='')
        page = request.GET.get('page', default=1)
        page = int(page)
        order_by = request.GET.get('order_by', default='release_time')
        order_by = '-' + order_by
        discussion_list = Discussion.objects.filter(title__contains=keyword).order_by(order_by)[(page - 1) * 20: page * 20]
        discussion_count = Discussion.objects.count()
        page_count = (discussion_count + 19) // 20
        pagination = get_pagination(page, page_count)
        data = {
            'discussion_list': discussion_list,
            'total': len(discussion_list),
            'pagination': pagination,
            'order_by': order_by,
        }
        return render(request, 'discussion_list.html', data)
    except Exception as e:
        return render(request, '404_page.html', {'error_msg': e,
                                                 'btn_msg': '返回首页'})


@method_decorator(login_required(login_url='/account/login'), name='dispatch')
class Edit(View):
    def get(self, request):
        form = BlogForm()
        data = {
            'form': form,
        }
        return render(request, 'discussion_edit.html', data)

    def post(self, request):
        title = request.POST.get('title')
        content = request.POST.get('content')
        discussion_id = create_discussion_id()
        author = request.user
        Discussion.objects.create(id=discussion_id,
                                  title=title,
                                  author=author,
                                  content=content)
        data = {
            'msg': '发布成功！',
            'url': '/discussion/' + discussion_id,
            'btn_msg': '前往查看',
        }
        return render(request, 'hint.html', data)


def query_is_like(discussion_id, user):
    if user.is_anonymous:
        return False
    discussion = Discussion.objects.filter(id=discussion_id)[0]
    if DiscussionLike.objects.filter(discussion=discussion, user=user).exists():
        is_like = DiscussionLike.objects.filter(discussion=discussion, user=user)[0].status
        return is_like
    else:
        return False
    

def discussion_detail(request, discussion_id):
    try:
        discussion = Discussion.objects.all().get(id__exact=discussion_id)
    except:
        return render(request, 'discussion_detail.html', {'msg': 'discussion not found!'})
    if request.user.id != discussion.author.id:
        discussion.view_count += 1
    discussion.save()
    # discussion.content = markdown2.markdown(re.sub(r'\$\$(.+?)\$\$', change_formula, discussion.content))
    discussion.content = markdown.markdown(discussion.content, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    is_like = query_is_like(discussion.id, request.user)
    # is_favorite = query_is_favorite(discussion.id, request.user)
    form = CommentForm()
    comment_list = get_discussion_comment(discussion)
    data = {
        'discussion': discussion,
        'is_like': is_like,
        # 'is_favorite': is_favorite,
        'comment_list': comment_list,
        'form': form
    }
    return render(request, 'discussion_detail.html', data)