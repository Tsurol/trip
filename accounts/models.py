from random import randint

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _


# 重写模型管理器类UserManager
class AuthUserManager(BaseUserManager):
    def _create_user(self, username, email, password, phone, **extra_fields):
        user = self.model(**extra_fields)
        user.username = username
        user.email = email
        user.phone = phone
        user.set_password(password)
        with transaction.atomic():
            user.save(using=self._db)
            Profile.objects.create(user=user, username=username)
        return user

    def _create_superuser(self, username, password, **extra_fields):
        user = self.model(**extra_fields)
        user.username = username
        user.set_password(password)
        with transaction.atomic():
            user.save(using=self._db)
            Profile.objects.create(user=user, username=username)
        return user

    def create_user(self, username, password, email=None, phone=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, phone, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_superuser(username, password, **extra_fields)


class User(AbstractUser):
    """ 用户模型 """
    avatar = models.ImageField(_('avatar'), upload_to='avatar/%Y%m', null=True, blank=True)
    nickname = models.CharField(_('nickname'), max_length=32, unique=True)
    phone = models.CharField(_('phone number'), max_length=20, default=None, unique=True, null=True)
    email = models.EmailField(_('email address'), default=None, unique=True, null=True)

    objects = AuthUserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('User')
        db_table = 'accounts_user'

    def __str__(self):
        return self.username


class Profile(models.Model):
    SEX_CHOICE = (
        (1, '男'),
        (0, '女')
    )
    # 冗余字段
    username = models.CharField(_('username'), max_length=150, unique=True)
    real_name = models.CharField(_('real name'), max_length=32, null=True, blank=True)
    address = models.CharField(_('address'), max_length=255, null=True, blank=True)
    sex = models.SmallIntegerField(_('sex'), default=1, choices=SEX_CHOICE)
    age = models.SmallIntegerField(_('age'), default=0)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    user = models.OneToOneField(verbose_name=_('User related'), to=User,
                                on_delete=models.CASCADE, related_name='profile')

    class Meta:
        db_table = 'accounts_user_profile'
        verbose_name = '用户详细信息'
        verbose_name_plural = '用户详细信息'

    def __str__(self):
        return self.username


class LoginRecord(models.Model):
    username = models.CharField(_('username'), max_length=150, editable=False)
    ip = models.CharField(_('ip address'), max_length=50, null=True, blank=True)
    # 登录的来源
    source = models.CharField(_('source'), max_length=30, null=True, blank=True)
    # 登录的版本
    version = models.CharField(_('version'), max_length=30, null=True, blank=True)
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    user = models.ForeignKey(verbose_name=_('User related'), to=User,
                             on_delete=models.CASCADE, related_name='login_record')

    class Meta:
        db_table = 'accounts_login_record'
        verbose_name = '用户登录历史'
        verbose_name_plural = '用户登录历史'

    def __str__(self):
        return self.username
