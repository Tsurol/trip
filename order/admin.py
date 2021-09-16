from django.contrib import admin

from order.models import Order, OrderItem, Payment
from utils.admin_action import set_valid, set_invalid


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # 要显示的字段
    list_display = ("sn", 'buy_count', 'buy_amount', 'to_user', 'to_phone', 'types', 'status', 'user', 'is_valid')
    # 分页大小
    list_per_page = 40
    # 外键关联查询优化,关联的字段一次性查出，减少查询次数
    list_select_related = ('user',)
    # 快捷搜索
    list_filter = ('types', 'status')
    # 关联搜索(模糊匹配),可跨关联关系搜索
    search_fields = ('sn',)
    # fields需要编辑的字段列表/exclude不需要编辑的字段列表
    exclude = ('created_at', 'updated_at', 'user')
    actions = (set_valid, set_invalid)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    # 要显示的字段
    list_display = ("order", "flash_name", 'flash_img', 'flash_origin_price', 'flash_price', 'flash_discount',
                    'buy_count', 'buy_amount', 'status', 'user', "content_type", "object_id", "is_valid")
    # 分页大小
    list_per_page = 40
    # 外键关联查询优化,关联的字段一次性查出，减少查询次数
    list_select_related = ('user', 'order')
    # 快捷搜索
    list_filter = ('status',)
    # 关联搜索(模糊匹配),可跨关联关系搜索
    search_fields = ('order__sn',)
    # fields需要编辑的字段列表/exclude不需要编辑的字段列表
    exclude = ('created_at', 'updated_at', 'user', 'order', 'content_type', 'object_id')
    actions = (set_valid, set_invalid)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    # 要显示的字段
    list_display = ("amount", "pay_sn", 'third_sn', 'status', 'remark', 'user',
                    'order', "is_valid")
    # 分页大小
    list_per_page = 40
    # 外键关联查询优化,关联的字段一次性查出，减少查询次数
    list_select_related = ('user', 'order')
    # 快捷搜索
    list_filter = ('status',)
    # 关联搜索(模糊匹配),可跨关联关系搜索
    search_fields = ('order__sn',)
    # fields需要编辑的字段列表/exclude不需要编辑的字段列表
    exclude = ('created_at', 'updated_at', 'user', 'order')
    actions = (set_valid, set_invalid)
