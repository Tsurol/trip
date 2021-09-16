import json

from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.response import Response

from system.models import ImageRelated
from trip_1.enums import RespCode
from sight.models import Sight, Comment, SightTicket, SightInfo
from sight.serializers import SightSerializer, SightDetailSerializer, CommentSerializer, TicketSerializer, \
    SightInfoSerializer, TicketDetailSerializer, SightImageSerializer


def get_sight_list(is_hot, is_top, name, current_page, page_size):
    meta = {}
    objects = []
    try:
        query = Q(is_valid=True)
        # 热门景点
        if is_hot:
            query = query & Q(is_hot=True)
        # 精选景点
        if is_top:
            query = query & Q(is_top=True)
        # 景点名称搜索
        if name:
            query = query & Q(name__icontains=name)
        qs = Sight.objects.filter(query)
        if not qs:
            return RespCode.NotFound.value, {}, []
        paginator = Paginator(qs, page_size)
        page_data = paginator.page(current_page)
        objects = SightSerializer(page_data, many=True).data
        # 当前页码
        meta['current_page'] = current_page
        # 总页数
        meta['page_count'] = paginator.num_pages
        # 总记录数
        meta['total_count'] = paginator.count
        return RespCode.Succeed.value, meta, objects
    except Exception as e:
        print(e)
        return RespCode.Exception.value, {}, []


def get_sight_list_cache(is_hot, is_top, name, current_page, page_size):
    # 1.从缓存拿数据(热门景点或者精选景点)
    # 2.缓存拿不到再从数据库拿数据
    meta = {}
    objects = []
    try:
        query = Q(is_valid=True)
        # 热门景点
        if is_hot:
            try:
                data = cache.get('index_hot')
                if data:
                    # 将从REDIS中取出的字符串转成字典
                    data = eval(data)
                    # print(data)
                    # return JsonResponse(data, safe=False)
                    return RespCode.CacheSucceed.value, data
                else:
                    query = query & Q(is_hot=True)
            except Exception as e:
                print(e)
        # 精选景点
        if is_top:
            try:
                data = cache.get('index_top')
                if data:
                    data = eval(data)
                    # print(data)
                    # return JsonResponse(data, safe=False)
                    return RespCode.CacheSucceed.value, data
                else:
                    query = query & Q(is_top=True)
            except Exception as e:
                print(e)
        # 景点名称搜索
        if name:
            query = query & Q(name__icontains=name)
        qs = Sight.objects.filter(query)
        if not qs:
            return RespCode.NotFound.value, []
        paginator = Paginator(qs, page_size)
        page_data = paginator.page(current_page)
        objects = SightSerializer(page_data, many=True).data
        resp = {
            'code': 0,
            'meta': {
                'current_page': current_page,
                'page_count': paginator.num_pages,
                'total_count': paginator.count
            },
            'objects': objects
        }
        return RespCode.Succeed.value, resp
    except Exception as e:
        print(e)
        return RespCode.Exception.value, {}, []


def get_sight_detail(pk):
    try:
        query = Q(is_valid=True) & Q(id=pk)
        qs = Sight.objects.filter(query)
        if not qs:
            return RespCode.NotFound.value, {}, []
        objects = SightDetailSerializer(qs, many=True).data
        return RespCode.Succeed.value, {}, objects
    except Exception as e:
        print(e)
        return RespCode.Exception.value, {}, []


def get_comment_list(pk, current_page, page_size):
    meta = {}
    objects = []
    try:
        # 先查询并判断该景点是否存在
        sight_qs = Sight.objects.filter(is_valid=True, pk=pk)
        if not sight_qs:
            return RespCode.NotFound.value, {}, []
        # 再查询该景点下是否有评论
        query = Q(is_valid=True) & Q(sight_id=pk)
        comment_qs = Comment.objects.filter(query)
        if not comment_qs:
            return RespCode.NotFound.value, {}, []
        paginator = Paginator(comment_qs, page_size)
        page_data = paginator.page(current_page)
        objects = CommentSerializer(page_data, many=True).data
        meta['current_page'] = current_page
        meta['page_count'] = paginator.num_pages
        meta['total_count'] = paginator.count
        return RespCode.Succeed.value, meta, objects
    except Exception as e:
        print(e)
        return RespCode.Exception.value, {}, []


def get_image_list(pk, current_page, page_size):
    meta = {}
    objects = []
    try:
        sight_qs = Sight.objects.filter(is_valid=True, pk=pk)
        if not sight_qs:
            return RespCode.NotFound.value, {}, []
        # 复合类型
        image_qs = ImageRelated.objects.filter(content_type__app_label='sight', content_type__model='sight',
                                               object_id=pk)
        paginator = Paginator(image_qs, page_size)
        page_data = paginator.page(current_page)
        objects = SightImageSerializer(page_data, many=True).data
        meta['current_page'] = current_page
        meta['page_count'] = paginator.num_pages
        meta['total_count'] = paginator.count
        return RespCode.Succeed.value, meta, objects
    except Exception as e:
        print(e)
        return RespCode.Exception.value, {}, []


def get_ticket_list(pk, current_page, page_size):
    meta = {}
    objects = []
    try:
        # 先查询并判断该景点是否存在
        sight_qs = Sight.objects.filter(is_valid=True, pk=pk)
        if not sight_qs:
            return RespCode.NotFound.value, {}, []
        # 再查询该景点下是否有门票信息
        query = Q(is_valid=True) & Q(sight_id=pk)
        ticket_qs = SightTicket.objects.filter(query)
        if not ticket_qs:
            return RespCode.NotFound.value, {}, []
        paginator = Paginator(ticket_qs, page_size)
        page_data = paginator.page(current_page)
        objects = TicketSerializer(page_data, many=True).data
        meta['current_page'] = current_page
        meta['page_count'] = paginator.num_pages
        meta['total_count'] = paginator.count
        return RespCode.Succeed.value, meta, objects
    except Exception as e:
        print(e)
        return RespCode.Exception.value, {}, []


def get_sight_info(pk):
    meta = {}
    objects = []
    try:
        qs = SightInfo.objects.filter(pk=pk)
        if not qs:
            return RespCode.NotFound.value, {}, []
        objects = SightInfoSerializer(qs, many=True).data
        return RespCode.Succeed.value, meta, objects
    except Exception as e:
        print(e)
        return RespCode.Exception.value, {}, []


def get_ticket_detail(pk):
    try:
        # qs只有一条记录,所以序列化时many=True可不要
        qs = SightTicket.objects.get(pk=pk)
        if not qs:
            return RespCode.NotFound.value, {}
        objects = TicketDetailSerializer(qs).data
        resp = {
            'code': RespCode.Succeed.value,
            'data': objects,
            'message': 'Success'
        }
    except Exception as e:
        print(e)
        return RespCode.Exception.value, {}
    return RespCode.Succeed.value, resp
