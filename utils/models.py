from django.db import models
from django.utils.translation import ugettext_lazy as _


class CommonModel(models.Model):
    """ 模型公共类 """
    is_valid = models.BooleanField(_('if is valid'), default=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        abstract = True
