from django import forms

from comment.models import ArticleComment


class CommentForm(forms.ModelForm):
    class Meta:
        model = ArticleComment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(
                attrs={'class': 'form-control',
                       'aria-label': "With textarea",
                       'rows': '3',
                       'style': 'width: 100%;',
                       'placeholder': '请在此输入你的评论...',
                       'id': 'comment-content',
                       'required': True, })
        }


