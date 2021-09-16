from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _
from accounts.models import User
from order.choices import OrderStatus, OrderTypes, PayStatus
from utils.models import CommonModel


class Order(CommonModel):
    """ 订单信息 """
    sn = models.CharField(_('order no'), max_length=128, unique=True)
    buy_count = models.IntegerField(_('buy count'), default=1)
    buy_amount = models.FloatField(_('buy amount'))
    to_user = models.CharField(_('receiver'), max_length=32)
    to_area = models.CharField(_('area'), max_length=64, default='')
    to_address = models.CharField(_('detail address'), max_length=128, default='')
    to_phone = models.CharField(verbose_name='手机号', max_length=128)
    remark = models.CharField(_('remark'), max_length=64, null=True, blank=True)
    express_type = models.CharField(_('express type'), max_length=64, null=True, blank=True)
    express_no = models.CharField(_('express no'), max_length=64, null=True, blank=True)
    types = models.SmallIntegerField(_('order type'),
                                     choices=OrderTypes.choices,
                                     default=OrderTypes.SIGHT_TICKET)
    status = models.SmallIntegerField(_('order status'),
                                      choices=OrderStatus.choices,
                                      default=OrderStatus.SUBMIT)
    user = models.ForeignKey(verbose_name=_('User related'), to=User, on_delete=models.PROTECT, related_name='order_list')

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Order')
        db_table = 'Order'
        ordering = ['id']

    def __str__(self):
        return self.sn


class OrderItem(CommonModel):
    """ 订单明细 """
    flash_name = models.CharField(_('flash name'), max_length=128)
    flash_img = models.ImageField(_('flash img'), upload_to='order/%Y%m', max_length=512)
    flash_origin_price = models.FloatField(_('flash origin price'))
    flash_price = models.FloatField(_('flash price'))
    flash_discount = models.FloatField(_('flash discount'), default=10.0)
    buy_count = models.IntegerField(_('buy count'), default=1)
    buy_amount = models.FloatField(_('buy amount'))
    remark = models.CharField(_('remark'), max_length=64, null=True, blank=True)
    status = models.SmallIntegerField(_('order status'),
                                      choices=OrderStatus.choices,
                                      default=OrderStatus.SUBMIT)
    user = models.ForeignKey(verbose_name=_('User related'), to=User, on_delete=models.PROTECT, related_name='order_item_list')
    # 购物车的概念 todo:暂未实现
    # order = models.ForeignKey(verbose_name=_('Order related'), to=Order, on_delete=models.CASCADE, related_name='order_item_list')
    order = models.OneToOneField(verbose_name=_('Order related'), to=Order, on_delete=models.CASCADE, related_name='order_item')
    # 关联的模型
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name=_('model related'))
    # 具体对象的id
    object_id = models.PositiveIntegerField(_('object id'))
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = _('Order_item')
        verbose_name_plural = _('Order_item')
        db_table = 'Order_item'
        ordering = ['id']

    def __str__(self):
        return self.flash_name


class Payment(CommonModel):
    """ 支付凭证 """
    amount = models.FloatField(_('amount'), help_text='real pay')
    pay_sn = models.CharField(_('pay no'), max_length=32)
    third_sn = models.CharField(_('third pay sn'), max_length=128, null=True, blank=True)
    status = models.SmallIntegerField(_('pay status'),
                                      choices=PayStatus.choices,
                                      default=PayStatus.SUBMIT)
    meta = models.CharField(_('meta'), max_length=128, null=True, blank=True)
    remark = models.CharField(_('remark'), max_length=128, null=True, blank=True)
    user = models.ForeignKey(verbose_name=_('User related'), to=User, on_delete=models.CASCADE, related_name='payment_list')
    # 购物车的概念 todo:暂未实现
    # order = models.ForeignKey(verbose_name=_('Order related'), to=Order, on_delete=models.CASCADE, related_name='payment_list')
    order = models.OneToOneField(verbose_name=_('Order related'), to=Order, on_delete=models.CASCADE, related_name='payment_item')

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payment')
        db_table = 'Order_payment'
        ordering = ['id']

    def __str__(self):
        return self.id
