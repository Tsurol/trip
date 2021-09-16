# coding:utf-8

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

# 发信方的信息:发信邮箱,QQ邮箱授权码
from utils.exceptions import NetworkException

sender_email = '2656155887@qq.com'
sender_passwd = 'uqmcpadgribcebib'
# 发信服务器,端口号
smtp_server = 'smtp.qq.com'
port = 465
PROJECT_NAME = 'trip'


def send_email(to_email: str, verify_code: str):
    """

    :param to_email: 收件邮箱
    :param verify_code: 验证码
    :return:
    """
    # 邮件主题
    subject = "[trip] Please check your email code"
    try:
        mail_msg = MIMEMultipart()
        content = '您的邮箱验证码为：{} \n Please don`t report this email \n ---  {}  ---'.format(verify_code, PROJECT_NAME)
        mail_msg.attach(MIMEText(content, 'plain', 'utf-8'))
        mail_msg['From'] = sender_email
        mail_msg['Subject'] = Header(subject, 'utf-8')
        mail_msg['To'] = to_email
        try:
            # 开启发信服务，这里使用的是加密传输
            server = smtplib.SMTP_SSL(smtp_server)
            server.connect(smtp_server, port)
            # 登录发信邮箱
            server.login(sender_email, sender_passwd)
            # 发送邮件
            server.sendmail(sender_email, to_email, mail_msg.as_string())
            # 关闭服务器
            server.quit()
        except smtplib.SMTPException as e:
            print(e)
            raise NetworkException("SMTP Error")
    except Exception as e:
        print(e)
        raise NetworkException("SMTP Error")


if __name__ == '__main__':
    # Test代码
    send_email(to_email='zzlzzl996@126.com', verify_code='5555')
    print('ok')
