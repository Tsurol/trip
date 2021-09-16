from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from rest_framework.fields import SerializerMethodField

from accounts.models import User, LoginRecord, Profile
from trip_1.serializers import CustomFieldsSerializer


class UserSerializer(CustomFieldsSerializer):
    nickname = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'avatar', 'nickname')

    def get_nickname(self, obj):
        """ 用户昵称脱敏处理 """
        if not obj.nickname:
            return '匿名用户'
        return obj.nickname[:1] + "***"


class UserProfileSerializer(CustomFieldsSerializer):
    class Meta:
        model = Profile
        fields = ('real_name', 'sex', 'age', 'user')


class UserLoginRecordSerializer(CustomFieldsSerializer):
    created_at = serializers.SerializerMethodField(label=_('login at'), read_only=True)

    class Meta:
        model = LoginRecord
        fields = ('ip', 'address', 'source', 'version', 'created_at', 'user')

    def get_created_at(self, obj):
        """ 获取评论的创建时间-年月日 """
        return obj.created_at.strftime('%Y-%m-%d %H-%M-%S')


class UserDetailSerializer(CustomFieldsSerializer):
    # profile = UserProfileSerializer()
    # login_record = UserLoginRecordSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone', 'nickname', 'avatar')
