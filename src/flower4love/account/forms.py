# coding=utf-8

from django import forms


class RegistertForm(forms.Form):
    username = forms.RegexField(label='登录账号', max_length=11, regex=r'^1\d{10}$',
                                widget=forms.TextInput(attrs={'placeholder': u'请填写您的常用手机号码作用登录账号'}),
                                error_message=(u'手机号码格式不正确'))
    name = forms.CharField(label='称呼/姓名', max_length=10,
                           widget=forms.TextInput(attrs={'placeholder': u'请填写您的姓名'}))
    email = forms.CharField(label='常用邮箱', max_length=100,
                            widget=forms.TextInput(attrs={'placeholder': u'请填写您的常用邮箱'}))
    password1 = forms.CharField(label='密码',
                                widget=forms.PasswordInput(attrs={'placeholder': u'长度6~20位，至少包含数字、字母、字符中的两种  '}))
    password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput(attrs={'placeholder': u'请再次输入密码 '}))
    check_code = forms.CharField(label='验证码', max_length=4,
                                 widget=forms.TextInput(
                                     attrs={'class': 'input-text auth-code-input', 'placeholder': '验证码'}))

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return self.cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=11,
                               widget=forms.TextInput(attrs={'placeholder': u'请输入您的注册手机'}))
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(attrs={'placeholder': u'请输入您的登录密码'}))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())


class PasswordFindForm(forms.Form):
    email = forms.EmailField(label='电子邮件',
                             widget=forms.TextInput(attrs={'placeholder': u'注册邮箱'}))
    check_code = forms.CharField(label='验证码', max_length=4,
                                 widget=forms.TextInput(attrs={'class': 'input-text', 'placeholder': u'验证码'}))


class modifypasswordForm(forms.Form):
    oldpassword = forms.CharField(label='原密码', required=True, error_messages={'required': '请输入原密码'},
                                  widget=forms.PasswordInput(attrs={'placeholder': u'请输入账户密码', 'class': 'input-text',
                                                                    'onblur': "checkdata('id_oldpassword')"}))
    password1 = forms.CharField(label='密码',
                                widget=forms.PasswordInput(attrs={'placeholder': u'请输入账户新密码', 'class': 'input-text',
                                                                  'onblur': "checkdata('id_password1')"}))
    password2 = forms.CharField(label='确认密码',
                                widget=forms.PasswordInput(attrs={'placeholder': u'请再次输入账户新密码', 'class': 'input-text',
                                                                  'onblur': "checkdata('id_password2')"}))

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"所有项都为必填项")
        elif self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise forms.ValidationError(u"两次输入的新密码不一样")
        else:
            cleaned_data = super(modifypasswordForm, self).clean()
        return cleaned_data


class PasswordResetForm(forms.Form):
    new_password = forms.CharField(label='密码',
                                   widget=forms.PasswordInput(attrs={'placeholder': u'请输入账户新密码', 'class': 'input-text',
                                                                     'onblur': "checkdata('new_password')"}))
