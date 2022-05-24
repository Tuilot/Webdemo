import re

from django import forms

from common_lib.account_utils import calc_md5
from account.models import Account


class UserBaseInfo(forms.Form):
    username = forms.CharField(label='用户名：', max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'username'}
    ))
    email = forms.CharField(label='邮箱：', widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'email'}
    ))
    school = forms.CharField(label='学校：', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'id': 'school'}
    ))
    phone_number = forms.CharField(label='手机号：', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'id': 'phone_number'}
    ))


def email_check(email):
    if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) is not None:
        return True
    else:
        return False


class RegistrationForm(forms.Form):
    email = forms.CharField(label='邮箱：', widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'email'}
    ))
    username = forms.CharField(label='用户名：', max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'username'}
    ))
    password1 = forms.CharField(label='密码：', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'id': 'password1'}
    ))
    password2 = forms.CharField(label='确认密码：', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'id': 'password2'}
    ))

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if len(username) > 16:
            raise forms.ValidationError("用户名长度应低于16个字符")
        else:
            filter_result = Account.objects.filter(username__exact=username)
            if len(filter_result) > 0:
                raise forms.ValidationError("该用户名已存在")

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email_check(email):
            filter_result = Account.objects.filter(email__exact=email)
            if len(filter_result) > 0:
                raise forms.ValidationError("该邮箱已被注册")
        else:
            raise forms.ValidationError("邮箱地址无效")

        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if len(password1) < 8:
            raise forms.ValidationError("密码长度应介于8-16位")
        elif len(password1) > 16:
            raise forms.ValidationError("密码长度应介于8-16位")

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("两次密码不匹配，请重新输入")

        return password2


class LoginForm(forms.Form):
    email = forms.CharField(label='邮箱：', widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'email'}
    ))
    password = forms.CharField(label='密码：', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'id': 'password'}
    ))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email

    def clean_password(self):
        email = self.cleaned_data.get('email')
        password = calc_md5(self.cleaned_data.get('password'))
        try:
            user = Account.objects.get(email__exact=email)
            save_password = user.password
            if password and save_password and password != save_password:
                raise forms.ValidationError("邮箱或密码不正确")
        except:
            raise forms.ValidationError("邮箱或密码不正确")

        return password


class EditUserInfoForm(forms.Form):
    edit_username = forms.CharField()
    edit_email = forms.EmailField()
    edit_phone_number = forms.CharField(required=False)
    edit_school = forms.CharField(required=False)
    edit_real_name = forms.CharField(required=False)
    edit_motto = forms.CharField(required=False)
    edit_sex = forms.CharField(required=False)
