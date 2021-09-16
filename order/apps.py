from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class OrderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'order'
    verbose_name = _('order')
    verbose_name_plural = _('order')
