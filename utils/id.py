# coding:utf-8
import random
import string
from uuid import uuid1

from django.utils.timezone import now


class Generate:
    """
    ID类生成
    """

    @staticmethod
    def _get_id(size, chars):
        return ''.join(random.choice(chars) for _ in range(size))

    @staticmethod
    def get_uid():
        return uuid1().hex

    @classmethod
    def get_ref_code(cls):
        """ 生成六位字母 """
        return cls._get_id(6, string.ascii_uppercase)

    @classmethod
    def get_verify_code(cls):
        """ 生成验证码 """
        return cls._get_id(size=4, chars=string.digits)

    def get_trans_id(self, date=None, third=False):
        """ 生成交易流水号或第三方支付凭证 """
        if date is None:
            date = now()
        if third:
            # 第三方支付凭证
            str_date = date.strftime('%Y%m%d%H%M%S%f')
            str_rand = random.randint(1000, 9999)
            return '{}{}{}'.format('third', str_date, str_rand)
        else:
            # 交易流水号
            str_date = date.strftime('%Y%m%d%H%M%S%f')
            str_rand = random.randint(1000, 9999)
            return '{}{}'.format(str_date, str_rand)


