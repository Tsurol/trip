from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import ugettext_lazy as _
from trip_1.enums import RespCode
from utils.response import reformat_resp, error_resp, reformat_resp__
from sight import serializers
from sight.business import get_sight_list, get_sight_detail, get_comment_list, get_ticket_list, get_sight_info, \
    get_ticket_detail, get_image_list, get_sight_list_cache
from sight.models import Sight


class GetSightView(APIView):
    """ 景点列表接口 """
    permission_classes = [AllowAny]

    def get(self, request):
        is_hot = request.query_params.get('is_hot', None)
        is_top = request.query_params.get('is_top', None)
        name = request.query_params.get('name', None)
        # 当前页码
        current_page = int(request.query_params.get('page', 1))
        code, meta, objects = get_sight_list(is_hot, is_top, name, current_page, page_size=5)
        if code == RespCode.Succeed.value:
            return reformat_resp(code, meta, objects, 'Succeed')
        elif code == RespCode.NotFound.value:
            return error_resp(code, _('Resource not found'))
        else:
            return error_resp(code, _('Server exception, please try again'))


class GetSightCacheView(APIView):
    """ 景点列表接口缓存优化 """
    permission_classes = [AllowAny]

    def get(self, request):
        is_hot = request.query_params.get('is_hot', None)
        is_top = request.query_params.get('is_top', None)
        name = request.query_params.get('name', None)
        # 当前页码
        current_page = int(request.query_params.get('page', 1))
        code, data = get_sight_list_cache(is_hot, is_top, name, current_page, page_size=20)
        if code == RespCode.Succeed.value:
            return Response(data)
        elif code == RespCode.CacheSucceed.value:
            return Response(data)
        elif code == RespCode.NotFound.value:
            return error_resp(code, _('Resource not found'))
        else:
            return error_resp(code, _('Server exception, please try again'))


class GetSightDetail(APIView):
    """ 景点详请接口 """
    permission_classes = [AllowAny]

    def get(self, request, pk):
        code, meta, objects = get_sight_detail(pk)
        if code == RespCode.Succeed.value:
            return reformat_resp__(objects)
        elif code == RespCode.NotFound.value:
            return error_resp(code, _('Resource not found'))
        else:
            return error_resp(code, _('Server exception, please try again'))


class GetCommentView(APIView):
    """ 景点评论列表接口 """
    permission_classes = [AllowAny]

    def get(self, request, pk):
        current_page = int(request.query_params.get('page', 1))
        # 默认加载前十条数据
        page_size = int(request.query_params.get('limit', 10))
        code, meta, objects = get_comment_list(pk, current_page, page_size=page_size)
        if code == RespCode.Succeed.value:
            return reformat_resp(code, meta, objects, 'Succeed')
        elif code == RespCode.NotFound.value:
            return error_resp(code, _('Resource not found'))
        else:
            return error_resp(code, _('Server exception, please try again'))


class GetTicketView(APIView):
    """ 景点门票列表接口 """
    permission_classes = [AllowAny]

    def get(self, request, pk):
        current_page = int(request.query_params.get('page', 1))
        code, meta, objects = get_ticket_list(pk, current_page, page_size=5)
        if code == RespCode.Succeed.value:
            return reformat_resp(code, meta, objects, 'Succeed')
        elif code == RespCode.NotFound.value:
            return error_resp(code, _('Resource not found'))
        else:
            return error_resp(code, _('Server exception, please try again'))


class GetSightInfoView(APIView):
    """ 景点介绍接口 """
    permission_classes = [AllowAny]

    def get(self, request, pk):
        code, meta, objects = get_sight_info(pk)
        if code == RespCode.Succeed.value:
            return reformat_resp(code, meta, objects, 'Succeed')
        elif code == RespCode.NotFound.value:
            return error_resp(code, _('Resource not found'))
        else:
            return error_resp(code, _('Server exception, please try again'))


class GetTicketDetailView(APIView):
    """ 门票详情信息接口 """
    permission_classes = [AllowAny]

    def get(self, request, pk):
        code, resp = get_ticket_detail(pk)
        if code == RespCode.Succeed.value:
            return Response(resp)
        elif code == RespCode.NotFound.value:
            return error_resp(code, _('Resource not found'))
        else:
            return error_resp(code, _('Server exception, please try again'))


class GetImageListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        current_page = int(request.query_params.get('page', 1))
        code, meta, objects = get_image_list(pk, current_page, page_size=10)
        if code == RespCode.Succeed.value:
            return reformat_resp(code, meta, objects, 'Succeed')
        elif code == RespCode.NotFound.value:
            return error_resp(code, _('Resource not found'))
        else:
            return error_resp(code, _('Server exception, please try again'))
