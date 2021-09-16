from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _
from accounts.models import User
from utils.models import CommonModel


class Slider(CommonModel):
    """ 轮播图 """
    name = models.CharField(_('name'), max_length=64)
    desc = models.CharField(_('desc'), max_length=256, null=True, blank=True)
    types = models.SmallIntegerField(_('type'), default=10, help_text='10默认是首页轮播')
    img = models.ImageField(_('img url'), max_length=256, upload_to='slider/%Y%m')
    start_time = models.DateTimeField(_('start time'), null=True, blank=True)
    end_time = models.DateTimeField(_('end time'), null=True, blank=True)
    reorder = models.SmallIntegerField(_('reorder'), default=0, help_text='数字越大靠前')
    target_url = models.CharField(_('link to'), max_length=256, null=True, blank=True)

    class Meta:
        verbose_name = _('Slider')
        verbose_name_plural = _('Slider')
        db_table = 'system_slider'
        # 按reorder降序排列
        ordering = ['-reorder']

    def __str__(self):
        return self.name


class ImageRelated(CommonModel):
    """ 图片关联 """
    """
    景点需要关联图片，评论中也需要关联图片，就可以使用复合类型。
    通过content_type知道关联的是哪个模型，object_id知道关联的是表中的某条记录的id
    """
    img = models.ImageField(_('img url'), upload_to='file/%Y%m', max_length=256)
    # 图片说明
    summary = models.CharField(_('summary'), max_length=32, null=True, blank=True)
    # 上传图片的用户
    user = models.ForeignKey(User,
                             on_delete=models.SET(None),
                             related_name='upload_images',
                             verbose_name=_('who upload'),
                             null=True)
    # 关联的模型
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name=_('model related'))
    # 具体对象的id
    object_id = models.IntegerField(_('object id'))
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = _('ImageRelated')
        verbose_name_plural = _('ImageRelated')
        db_table = 'system_image_related'
        ordering = ['id']

    def __str__(self):
        return str(self.id)
