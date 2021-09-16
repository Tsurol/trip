from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from django.utils.translation import gettext_lazy as _
from order.business import order_submit, get_order_detail, order_pay_submit, order_cancel, order_delete, get_my_orders
from trip_1.enums import RespCode
from utils.id import Generate
from utils.response import error_resp, reformat_resp_, reformat_resp


class OrderSubmitView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """ 下订单 """
        try:
            ticket_id = int(request.data.get('ticket_id', None))
            play_date = request.data.get('play_date', None)
            buy_count = int(request.data.get('buy_count', None))
            to_phone = request.data.get('to_phone', None)
            to_user = request.data.get('to_user', None)
            code, resp = order_submit(ticket_id, play_date, buy_count, to_phone, to_user, request)
            if code == RespCode.Succeed.value:
                return Response(resp)
            else:
                return error_resp(code, resp)
        except Exception as e:
            print(e)
        return error_resp(RespCode.Exception.value, _('Server exception, please try again'))


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, sn):
        """ 订单支付页面 """
        try:
            code, resp = get_order_detail(request, sn)
            if code == RespCode.Succeed.value:
                return Response(resp)
            else:
                return error_resp(code, resp)
        except Exception as e:
            print(e)
            return error_resp(RespCode.Exception.value, _('Server exception, please try again'))

    def delete(self, request, sn):
        """ 订单删除(逻辑删除) """
        try:
            code, resp = order_delete(request, sn)
            if code == RespCode.Succeed.value:
                return reformat_resp_(code, resp, 'Success')
            else:
                return error_resp(code, resp)
        except Exception as e:
            print(e)
            return error_resp(RespCode.Exception.value, _('Server exception, please try again'))

    def put(self, request, sn):
        """ 取消订单 """
        try:
            code, resp = order_cancel(request, sn)
            if code == RespCode.Succeed.value:
                return reformat_resp_(code, resp, 'Success')
            else:
                return error_resp(code, resp)
        except Exception as e:
            print(e)
            return error_resp(RespCode.Exception.value, _('Server exception, please try again'))

    def post(self, request, sn):
        """ 立即支付 """
        try:
            code, resp = order_pay_submit(request, sn)
            if code == RespCode.Succeed.value:
                return Response(resp)
            else:
                return error_resp(code, resp)
        except Exception as e:
            print(e)
            return error_resp(RespCode.Exception.value, _('Server exception, please try again'))


class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """ 我的订单列表 """
        try:
            current_page = int(request.query_params.get('page', 1))
            limit = int(request.query_params.get('limit', 10))
            status = int(request.query_params.get('status'))
            code, meta, objects = get_my_orders(request, status, current_page, limit)
            if code == RespCode.Succeed.value:
                return reformat_resp(code, meta, objects, 'Success')
            else:
                return error_resp(code, objects)
        except Exception as e:
            print(e)
            return error_resp(RespCode.Exception.value, _('Server exception, please try again'))
