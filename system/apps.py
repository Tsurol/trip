from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'system'
    verbose_name = _('system')
    verbose_name_plural = _('system')
