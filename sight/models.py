from ckeditor.fields import RichTextField
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import ugettext_lazy as _
from accounts.models import User
from order.models import OrderItem
from sight.choices import TicketTypes, TicketStatus, EntryWay
from system.models import ImageRelated
from utils.models import CommonModel


class Sight(CommonModel):
    """ 景点基础信息 """
    name = models.CharField(_('name'), max_length=64)
    desc = models.CharField(_('desc'), max_length=64)
    main_img = models.ImageField(_('main_img'), upload_to='sight/%Y%m', max_length=512)
    banner_img = models.ImageField(_('banner_img'), upload_to='sight/%Y%m', max_length=512)
    # content = models.TextField(_('content'))
    content = RichTextField(_('content'))
    score = models.FloatField(_('score'), default=5)
    province = models.CharField(_('province'), max_length=32)
    city = models.CharField(_('city'), max_length=32)
    area = models.CharField(_('area'), max_length=32, null=True, blank=True)
    town = models.CharField(_('town'), max_length=32, null=True, blank=True)
    min_price = models.FloatField(_('min_price'), default=0)
    is_top = models.BooleanField(_('is_top'), default=False)
    is_hot = models.BooleanField(_('is_hot'), default=False)

    images = GenericRelation(ImageRelated,
                             verbose_name='关联的图片',
                             related_query_name='sight_images')

    class Meta:
        verbose_name = _('Sight')
        verbose_name_plural = _('sight')
        db_table = 'sight'
        # 最新更新的排前面
        # ordering = ['-updated_at']
        ordering = ['id']

    def __str__(self):
        return self.name


class SightInfo(models.Model):
    """ 景点详情信息 """
    sight = models.OneToOneField(verbose_name=_('Sight related'), to=Sight, on_delete=models.CASCADE,
                                 related_name='info')
    entry_explain = RichTextField(_('entry_explain'), max_length=1024, blank=True, null=True)
    play_way = RichTextField(_('play_types'), blank=True, null=True)
    tips = RichTextField(_('tips'), blank=True, null=True)
    traffic = RichTextField(_('traffic'), blank=True, null=True)

    class Meta:
        verbose_name = _('SightInfo')
        verbose_name_plural = _('SightInfo')
        db_table = 'sight_info'

    def __str__(self):
        return str(self.id)


class SightTicket(CommonModel):
    """ 景点门票信息 """
    sight = models.ForeignKey(verbose_name=_('Sight related'), to=Sight, related_name='tickets',
                              on_delete=models.PROTECT)
    name = models.CharField(_('name'), max_length=128)
    desc = models.CharField(_('desc'), max_length=64, null=True, blank=True)
    types = models.SmallIntegerField(_('types'),
                                     choices=TicketTypes.choices,
                                     default=TicketTypes.ADULT,
                                     help_text=_('default adult ticket'))
    price = models.FloatField(_('original price'))
    discount = models.FloatField(_('discount'), default=10)
    total_stock = models.PositiveIntegerField(_('total stock'), default=0)
    remain_stock = models.PositiveIntegerField(_('remain stock'), default=0)
    expire_date = models.IntegerField(_('expire date'), default=1)
    return_policy = models.CharField(_('return policy'), max_length=64, default='with condition')
    has_invoice = models.BooleanField(_('if has invoice'), default=True)
    entry_way = models.SmallIntegerField(_('entry_way'),
                                         choices=EntryWay.choices,
                                         default=EntryWay.BY_TICKET)
    # tips:预订须知
    tips = RichTextField(_('tips'), null=True, blank=True)
    remark = RichTextField(_('remark'), null=True, blank=True)
    status = models.SmallIntegerField(_('状态'),
                                      choices=TicketStatus.choices,
                                      default=TicketStatus.OPEN)
    order_items = GenericRelation(OrderItem,
                                  verbose_name='关联的订单',
                                  related_query_name='ticket')

    class Meta:
        db_table = 'sight_ticket'
        verbose_name = _('SightTicket')
        verbose_name_plural = _('SightTicket')
        ordering = ['id']

    @property
    def sell_price(self):
        """ 销售价 = 原价 x 折扣 """
        return self.price * self.discount / 10

    def __str__(self):
        return str(self.id)


class Comment(CommonModel):
    """ 评论及回复 """
    user = models.ForeignKey(to=User, verbose_name=_('commentator'),
                             related_name='comments',
                             on_delete=models.CASCADE)
    sight = models.ForeignKey(Sight, verbose_name=_('sight'),
                              related_name='comments',
                              on_delete=models.CASCADE)
    content = models.TextField(_('content'), blank=True, null=True)
    is_top = models.BooleanField(_('if is top'), default=False)
    love_count = models.IntegerField(_('love count'), default=0)
    score = models.FloatField(_('score'), default=5)

    ip_address = models.CharField(_('ip address'), blank=True, null=True, max_length=64)
    is_public = models.SmallIntegerField(_('if is public'), default=1)
    reply = models.ForeignKey(to='self', blank=True, null=True,
                              related_name='reply_comment',
                              verbose_name=_('reply for comment'),
                              on_delete=models.CASCADE)

    images = GenericRelation(to=ImageRelated,
                             verbose_name=_('img related'),
                             related_query_name="comment_images")

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comment')
        db_table = 'sight_comment'
        ordering = ['-love_count', '-created_at']

    def __str__(self):
        return str(self.id)
