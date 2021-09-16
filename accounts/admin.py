from django import forms
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin

from accounts.forms import ProfileEditForm, LoginRecordForm
from accounts.models import Profile, LoginRecord, User


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """ 用户详细信息 """
    # 要显示的字段
    list_display = ("format_username", 'sex', 'age', 'address', 'real_name', 'updated_at', 'user')
    # 分页大小
    list_per_page = 15
    # 外键关联查询优化,关联的字段一次性查出，减少查询次数
    list_select_related = ('user',)
    # 快捷搜索
    list_filter = ('sex',)
    # 关联搜索(模糊匹配),可跨关联关系搜索
    search_fields = ('username', 'user__nickname')
    # fields需要编辑的字段列表/exclude不需要编辑的字段列表
    exclude = ('created_at', 'updated_at', 'username', 'user')
    # 自定义表单验证
    form = ProfileEditForm

    # 格式化显示字段内容
    def format_username(self, obj):
        """用户名脱敏处理"""
        return "***" + obj.username[7:]

    format_username.short_description = '用户名'


@admin.register(LoginRecord)
class LoginRecordAdmin(admin.ModelAdmin):
    """ 用户登录历史记录 """
    # 要显示的字段
    list_display = ("format_username", 'ip', 'source', 'version', 'created_at', 'user')
    exclude = ("format_username", 'ip', 'source', 'version', 'created_at', 'user')
    list_per_page = 40
    list_select_related = ('user',)
    list_filter = ('ip',)
    search_fields = ('username', 'user__nickname')
    form = LoginRecordForm

    # 格式化显示字段内容
    def format_username(self, obj):
        """用户名脱敏处理"""
        return "***" + obj.username[7:]

    format_username.short_description = '用户名'


@admin.register(User)
class UserAdmin(UserAdmin):
    """ 用户基础信息管理 """
    # 要显示的字段
    list_display = ("format_username", "nickname", "phone", "email", "is_staff", "is_active", "date_joined")
    list_per_page = 20
    list_filter = ('is_active', "is_staff")
    search_fields = ('username', 'nickname')
    # 新增的表单
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('nickname',)}),
    )
    # 修改的表单
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('nickname', 'avatar')}),
    )

    actions = ('disable_user', 'enable_user')

    def disable_user(self, request, queryset):
        """ 批量禁用用户 """
        queryset.update(is_active=False)
        messages.success(request, '操作成功')

    disable_user.short_description = '批量禁用用户'

    def enable_user(self, request, queryset):
        """ 批量启用用户 """
        queryset.update(is_active=True)
        messages.success(request, '操作成功')

    enable_user.short_description = '批量启用用户'

    # 格式化显示字段内容
    def format_username(self, obj):
        """用户名脱敏处理"""
        return "***" + obj.username[7:]

    format_username.short_description = '用户名'
