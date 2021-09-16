from django.conf import settings
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.bussiness import get_user_list, set_verify_code, register_user, login_user, get_user_info
from trip_1.enums import RespCode
from utils.email_service import send_email
from utils.id import Generate
from utils.phone_service import send_phone
from utils.response import reformat_resp, error_resp, reformat_resp_
from django.utils.translation import ugettext_lazy as _


class SendEmailCodeView(APIView):
    """ 发送邮箱验证码 """
    permission_classes = [AllowAny]

    def get(self, request):
        email = request.query_params.get("email", "")
        if not email:
            return error_resp(RespCode.BusinessError, "email params not found")
        key = 'verify_code_email:{}'.format(email)
        code = Generate.get_verify_code()  # code->str
        data = {}
        if not settings.DEBUG:
            send_email(email, code)
            data['code'] = code
            # data:{'code': 'xxxx'}
        else:
            data.update(code=code)  # data:{'code': 'xxxx'}
        # 将key和code存入redis缓存
        set_verify_code(key, code)
        return reformat_resp(RespCode.Succeed, {}, data, 'Success')


class SendPhoneCodeView(APIView):
    """ 发送手机验证码 """
    permission_classes = [AllowAny]

    def get(self, request):
        phone = request.query_params.get("phone", "")
        if not phone:
            return error_resp(RespCode.BusinessError, "phone params not found")
        key = 'verify_code_phone:{}'.format(phone)
        code = Generate.get_verify_code()  # code->str
        data = {}
        if not settings.DEBUG:
            send_phone(phone, code)
            data['code'] = code
            # data:{'code': 'xxxx'}
        else:
            data.update(code=code)  # data:{'code': 'xxxx'}
        set_verify_code(key, code)
        return reformat_resp(RespCode.Succeed, {}, data, 'Success')


class RegisterView(APIView):
    """ 用户注册接口 """
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            # email和phone任选其一进行注册
            email = request.data.get('email', None)
            phone = request.data.get('phone', None)
            nickname = request.data.get('nickname', None)
            password = request.data.get('password', None)
            code = request.data.get('code', None)
            code, resp = register_user(email, phone, nickname, password, code)
            if code == RespCode.Succeed.value:
                return Response(resp)
            else:
                return error_resp(code, resp)
        except Exception as e:
            print(e)
        return error_resp(RespCode.Exception.value, _('Server exception, please try again'))


class LoginView(APIView):
    """ 用户登录接口 """
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            # 1.邮箱+验证码 todo:前端暂时没有实现
            # 2.手机号+验证码
            # 3.用户名+密码
            email = request.data.get('email', None)
            phone = request.data.get('phone', None)
            code = request.data.get('code', None)
            username = request.data.get('username', None)
            password = request.data.get('password', None)
            code, resp = login_user(email, phone, code, username, password, request)
            if code == RespCode.Succeed.value:
                return Response(resp)
            else:
                return error_resp(code, resp)
        except Exception as e:
            print(e)
        return error_resp(RespCode.Exception.value, 'Exception')


class GetUserListView(APIView):
    """ 用户列表接口 """
    permission_classes = [IsAdminUser]

    def get(self, request):
        code, meta, objects = get_user_list(request)
        if code == RespCode.Succeed.value:
            return reformat_resp(code, meta, objects, 'Succeed')
        elif code == RespCode.NotFound.value:
            return error_resp(code, _('Resource not found'))
        else:
            return error_resp(code, _('Server exception, please try again'))


class GetUserInfoView(APIView):
    """ 用户信息接口 """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        code, resp = get_user_info(request)
        if code == RespCode.Succeed.value:
            return Response(resp)
        elif code == RespCode.NotFound.value:
            return error_resp(code, _('Resource not found'))
        else:
            return error_resp(code, _('Server exception, please try again'))
