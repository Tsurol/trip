# coding:utf-8

import re

# 表单验证类
from utils.exceptions import UserNotFoundException


class VerifyUtil:
    @staticmethod
    def verify_phone(phone):
        # 验证手机号码格式
        reg = r'^1[3-9]\d{9}$'
        return re.match(reg, phone)

    @staticmethod
    def verify_email(email):
        # 验证邮箱格式
        reg = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
        return re.match(reg, email)

    def verify_user(self, request):
        user = request.user
        if not user:
            raise UserNotFoundException("user not found")
        else:
            if not user.is_active:
                raise UserNotFoundException("user not found")
        return user


if __name__ == '__main__':
    # Test
    v = VerifyUtil()
    res = v.verify_phone('13778260466')
    res1 = v.verify_email('hello2131@163.com')
