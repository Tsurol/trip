from django import forms

from accounts.models import Profile, LoginRecord


class ProfileEditForm(forms.ModelForm):
    """ 用户详细信息编辑 """

    class Meta:
        model = Profile
        fields = ('real_name', 'sex', 'age')

    def clean_age(self):
        """ 验证用户年龄 """
        age = self.cleaned_data['age']
        if int(age) >= 120 or int(age) <= 1:
            raise forms.ValidationError("年龄只能在1~120之间")
        return age


class LoginRecordForm(forms.ModelForm):
    """ 用户登录历史 """

    class Meta:
        model = LoginRecord
        fields = ('ip',)

    def save(self, commit=False):
        obj = super().save(commit)
        # 保存数据时做一些其他的业务逻辑处理
        if not obj.source:
            obj.source = 'web'
            obj.save()
        return obj
