import json

from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache
from django.db import transaction
from django.db.models import Q
from accounts.models import User, LoginRecord
from accounts.serializers import UserSerializer, UserDetailSerializer, UserProfileSerializer
from trip_1.enums import RespCode
from utils.id import Generate
from utils.token import get_token_for_user
from utils.verify import VerifyUtil
from utils.pagination import MyPagination
from django.utils.translation import gettext_lazy as _


def get_user_info(request):
    try:
        user = request.user
        if user.is_active is False:
            return RespCode.NotFound.value, {}, []
        # resp = {}
        # resp['code'] = RespCode.Succeed.value
        # resp['user'] = UserDetailSerializer(user).data
        # resp['profile'] = UserProfileSerializer(user.profile).data
        # resp['message'] = 'Success'
        resp = {
            'code': RespCode.Succeed.value,
            'user': UserDetailSerializer(user).data,
            'profile': UserProfileSerializer(user.profile).data,
            'message': 'Success'
        }
        return RespCode.Succeed.value, resp
    except Exception as e:
        print(e)
        return RespCode.Exception.value, {}, []


def get_user_list(request):
    meta = {}
    objects = []
    try:
        query = Q(is_active=True)
        qs = User.objects.filter(query)
        if not qs:
            return RespCode.NotFound.value, {}, []
        # 实例化分页类
        page_obj = MyPagination()
        # 获取分页数据
        page_res = page_obj.paginate_queryset(queryset=qs, request=request)
        objects = UserDetailSerializer(page_res, many=True).data
        return RespCode.Succeed.value, meta, objects
    except Exception as e:
        print(e)
        return RespCode.Exception.value, {}, []


def set_verify_code(key, code):
    # 验证码有效期为60秒
    cache.set(key, json.dumps(code), 60)
    return None


def register_user(email, phone, nickname, password, code):
    is_email_exists = User.objects.filter(email=email).first()
    # is_phone_exists = User.objects.filter(phone=phone).first()
    is_nickname_exists = User.objects.filter(nickname=nickname).first()
    if is_nickname_exists:
        return RespCode.InvalidParams.value, _('Invalid nickname')
    # 实例化表单验证类
    verify_util = VerifyUtil()
    flag = 'phone'
    # 密码不得为空且必须大于四位数
    if password is None or len(password) < 4:
        return RespCode.InvalidParams.value, _('Invalid password')
    # 用户可选择手机号或者邮箱注册
    if phone == "" or phone is None:
        flag = 'email'
    if flag == 'email':
        # 验证邮箱格式
        verify_email = verify_util.verify_email(email=email)
        if not verify_email or is_email_exists:
            return RespCode.InvalidParams.value, _('Invalid email format')
        key = 'verify_code_email:{}'.format(email)
        cache_email_code = cache.get(key)
        if not cache_email_code:
            return RespCode.InvalidParams.value, _('Invalid email code')
        if code != json.loads(cache_email_code):
            return RespCode.InvalidParams.value, _('Invalid email code')
        # 邮箱验证通过!
        verify = True
    else:
        result = verify_util.verify_phone(phone=phone)
        if not result:
            return RespCode.InvalidParams.value, _('Invalid phone format')
        key = 'verify_code_phone:{}'.format(phone)
        cache_phone_code = cache.get(key)
        print(cache_phone_code)
        if not cache_phone_code:
            return RespCode.InvalidParams.value, _('Invalid phone code')
        if code != json.loads(cache_phone_code):
            return RespCode.InvalidParams.value, _('Invalid phone code')
        # 手机验证通过!
        verify = True
    if verify:
        # 默认用户名为注册的手机号或者邮箱
        if flag == 'phone':
            user = User.objects.create_user(username=phone, password=password,
                                            phone=phone, nickname=nickname)
        else:
            user = User.objects.create_user(username=email, password=password,
                                            email=email, nickname=nickname)
        resp = {}
        refresh_dict = get_token_for_user(user)
        # 用户注册即登录:减少用户操作
        try:
            resp['code'] = RespCode.Succeed.value
            resp['user'] = UserDetailSerializer(user).data
            resp['profile'] = UserProfileSerializer(user.profile).data
            resp['refresh'] = refresh_dict.get('refresh', '')
            resp['access'] = refresh_dict.get('access', '')
            resp['message'] = 'Success'
        except Exception as e:
            print(e)
        return RespCode.Succeed.value, resp


def login_user(email, phone, code, username, password, request):
    # 1.邮箱+验证码
    # 2.手机号+验证码
    # 3.用户名+密码
    flag = 'password'
    if password == '' or password is None:
        flag = 'code'
    if flag == 'code':
        if email == '' or email is None:
            flag = 'phone_code'
        else:
            flag = 'email_code'
    if flag == 'email_code':
        key = 'verify_code_email:{}'.format(email)
        cache_email_code = cache.get(key)
        if not cache_email_code:
            return RespCode.InvalidParams.value, _('Invalid email code')
        if code != json.loads(cache_email_code):
            return RespCode.InvalidParams.value, _('Invalid email code')
        verify = True
    elif flag == 'phone_code':
        key = 'verify_code_phone:{}'.format(phone)
        cache_phone_code = cache.get(key)
        if not cache_phone_code:
            return RespCode.InvalidParams.value, _('Invalid phone code')
        if code != json.loads(cache_phone_code):
            return RespCode.InvalidParams.value, _('Invalid phone code')
        verify = True
    else:
        user = User.objects.filter(username=username).first()
        if not user:
            return RespCode.NotFound.value, _('Resource not found')
        verify = check_password(password, user.password)
    if verify:
        user = User.objects.filter(username=username).first()
        if user.is_active is False:
            return RespCode.NotFound.value, _('Resource not found')
        custom_ip = request.META['REMOTE_ADDR']
        with transaction.atomic():
            resp = {}
            resp['code'] = RespCode.Succeed.value
            resp['user'] = UserDetailSerializer(user).data
            resp['profile'] = UserProfileSerializer(user.profile).data
            refresh_dict = get_token_for_user(user)
            resp['refresh'] = refresh_dict.get('refresh', '')
            resp['access'] = refresh_dict.get('access', '')
            resp['message'] = 'Success'
            LoginRecord.objects.create(user=user, username=user.username, ip=custom_ip)
        return RespCode.Succeed.value, resp
    else:
        return RespCode.InvalidParams.value, _("login error")
