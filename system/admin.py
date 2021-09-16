from django.contrib import admin

from system import models
from utils.admin_action import set_valid, set_invalid

admin.AdminSite.site_header = '旅游网后台管理'
admin.AdminSite.site_title = '旅游网后台管理'


@admin.register(models.Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('name', 'types', 'img', 'start_time', 'end_time', 'reorder', 'is_valid')
    list_per_page = 20
    list_filter = ('types',)
    search_fields = ('name',)
    actions = (set_valid, set_invalid)
    exclude = ('created_at', 'updated_at')


@admin.register(models.ImageRelated)
class ImageRelatedAdmin(admin.ModelAdmin):
    list_display = ('user', 'img', 'summary', 'content_type', 'object_id', 'is_valid')
    list_per_page = 20
    list_select_related = ('user',)
    search_fields = ('user__username',)
    actions = (set_valid, set_invalid)
    fields = ('img', 'summary', 'is_valid')

