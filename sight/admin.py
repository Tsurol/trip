import json

from django.contrib import admin
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage

from sight import models
from sight.models import Sight
from sight.serializers import SightSerializer
from utils.admin_action import set_invalid, set_valid
from utils.response import reformat_resp


@admin.register(models.Sight)
class SightAdmin(admin.ModelAdmin):
    list_display = ('name', 'main_img', 'banner_img', 'score', 'desc',
                    'province', 'city', 'min_price', 'is_hot', 'is_top', 'is_valid')
    list_per_page = 30
    list_filter = ('is_hot', 'is_top')
    search_fields = ('name', 'desc')
    exclude = ('created_at', 'updated_at')
    actions = (set_valid, set_invalid)

    def cache_top_sight(self):
        """ 缓存精选景点 """
        queryset = Sight.objects.filter(is_valid=True, is_top=True)
        try:
            paginator = Paginator(queryset, 20)
            current_page = 1
            # 第一页数据
            page_data = paginator.page(current_page)
            objects = SightSerializer(page_data, many=True).data
            key = 'index_top'
            resp = {
                'code': 0,
                'meta': {
                    'current_page': current_page,
                    'page_count': paginator.num_pages,
                    'total_count': paginator.count
                },
                'objects': objects,
                'from': 'redis'
            }
            cache.set(key, json.dumps(resp), 2 * 60 * 60)
        except EmptyPage as e:
            print('暂无数据', e)
        except Exception as e:
            print('缓存失败', e)

    def cache_hot_sight(self):
        """ 缓存热门景点 """
        queryset = Sight.objects.filter(is_valid=True, is_hot=True)
        try:
            paginator = Paginator(queryset, 20)
            # 第一页数据
            current_page = 1
            page_data = paginator.page(current_page)
            objects = SightSerializer(page_data, many=True).data
            key = 'index_hot'
            resp = {
                'code': 0,
                'meta': {
                    'current_page': current_page,
                    'page_count': paginator.num_pages,
                    'total_count': paginator.count
                },
                'objects': objects,
                'from': 'redis'
            }
            cache.set(key, json.dumps(resp), 2 * 60 * 60)
        except EmptyPage as e:
            print('暂无数据', e)
        except Exception as e:
            print('缓存失败', e)

    def save_form(self, request, form, change):
        """
        新增/修改时缓存数据
        :param request:
        :param form: 表单
        :param change: 表单是否发送改变
        :return:
        """
        obj = super().save_form(request, form, change)
        # 将热门景点/精选景点缓存到redis
        self.cache_top_sight()
        self.cache_hot_sight()
        return obj

    def delete_model(self, request, obj):
        """
        物理删除时更新redis缓存
        :param request:
        :param obj:
        :return:
        """
        self.cache_top_sight()
        self.cache_hot_sight()
        return super().delete_model(request, obj)


@admin.register(models.SightInfo)
class SightInfoAdmin(admin.ModelAdmin):
    list_display = ('sight', 'entry_explain', 'play_way', 'tips', 'traffic')
    list_per_page = 20
    search_fields = ('sight__name',)
    list_select_related = ('sight',)
    exclude = ('sight',)


@admin.register(models.SightTicket)
class SightTicketAdmin(admin.ModelAdmin):
    list_display = ('sight', 'name', 'desc', 'types', 'price', 'discount', 'sell_price', 'total_stock', 'remain_stock',
                    'expire_date', 'return_policy', 'has_invoice', 'entry_way', 'status', 'is_valid')
    list_per_page = 20
    search_fields = ('sight__name',)
    list_select_related = ('sight',)
    exclude = ('sight', 'created_at', 'updated_at')
    actions = (set_valid, set_invalid)

    def sell_price(self, obj):
        """用户名脱敏处理"""
        return obj.price * obj.discount / 10

    sell_price.short_description = '真实售价'


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'sight', 'content', 'love_count', 'score', 'is_valid')
    list_per_page = 20
    search_fields = ('sight__name', 'user__nickname')
    list_select_related = ('user', 'sight')
    exclude = ('sight', 'user', 'created_at', 'updated_at', 'reply')
    actions = (set_valid, set_invalid)
