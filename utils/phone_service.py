# coding:utf-8

from twilio.rest import Client

auth_token = '1c4c4eb4a4ad0ab03fa2d4133306957f'
account_sid = 'AC9dbe340064d2a3e8897e9920d3a3592f'
client = Client(account_sid, auth_token)


def send_phone(to_phone: str, verify_code: str):
    """

    :param to_phone: 收短信手机号
    :param verify_code: 验证码
    :return:
    """
    client.messages.create(
        from_='+13345390152',
        body=verify_code,
        to='+86{}'.format(to_phone)
    )
    print("Send phone-code Success")


if __name__ == '__main__':
    # Test
    send_phone("13508023081", "8816")

