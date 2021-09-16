from django.contrib import messages


def set_invalid(ModelAdmin, request, queryset):
    """ 批量禁用 """
    queryset.update(is_valid=False)
    messages.success(request, '操作成功')

set_invalid.short_description = '禁用所选对象'


def set_valid(ModelAdmin, request, queryset):
    """ 批量启用 """
    queryset.update(is_valid=True)
    messages.success(request, '操作成功')

set_valid.short_description = '启用所选对象'
