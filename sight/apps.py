from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SightConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sight'
    verbose_name = _('sight')
    verbose_name_plural = _('sight')
