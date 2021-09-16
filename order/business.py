# coding:utf-8
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import F
from order.choices import OrderStatus, PayStatus
from order.models import Order, OrderItem, Payment
from order.serializers import OrderSerializer, OrderItemSerializer, OrderDetailSerializer
from sight.choices import TicketStatus
from sight.models import SightTicket
from trip_1.enums import RespCode
from django.utils.translation import gettext_lazy as _
from utils.id import Generate
from utils.verify import VerifyUtil


def order_submit(ticket_id, play_date, buy_count, to_phone, to_user, request):
    """ 订单提交 """
    ticket = SightTicket.objects.filter(is_valid=True, id=ticket_id, status=TicketStatus.OPEN).first()
    if ticket is None:
        return RespCode.NotFound.value, _('ticket not found')
    else:
        if int(ticket.remain_stock) - buy_count < 0:
            return RespCode.BusinessError.value, _('ticket remain stock not enough')
    # 生成订单流水号
    g = Generate()
    # 当前用户
    v = VerifyUtil()
    user = v.verify_user(request=request)
    trans_id = g.get_trans_id()
    # 该门票的售价
    sell_price = ticket.sell_price
    # 购买门票的总价
    buy_amount = sell_price * buy_count
    # 门票名
    flash_name = ticket.name
    # 景点图片
    flash_img = ticket.sight.main_img
    # 原价
    flash_origin_price = ticket.price
    # 折扣
    flash_discount = ticket.discount
    # 出行时间备注
    remark = '出行时间：{}'.format(play_date)
    try:
        with transaction.atomic():
            order_qs = Order.objects.create(sn=trans_id,
                                            buy_count=buy_count,
                                            buy_amount=buy_amount,
                                            to_user=to_user,
                                            to_phone=to_phone,
                                            user=user)
            order_item_qs = OrderItem.objects.create(flash_name=flash_name,
                                                     flash_img=flash_img,
                                                     flash_origin_price=flash_origin_price,
                                                     flash_price=sell_price,
                                                     flash_discount=flash_discount,
                                                     buy_count=buy_count,
                                                     buy_amount=buy_amount,
                                                     remark=remark,
                                                     user=user,
                                                     order_id=order_qs.id,
                                                     content_type=ContentType.objects.get_for_model(SightTicket),
                                                     object_id=ticket_id)
            # F()函数从数据库操作层面修改数据，避免同时操作时的竞态条件
            ticket.remain_stock = F('remain_stock') - buy_count
            ticket.save()
            resp = {}
            data = OrderSerializer(order_qs).data
            resp['code'] = RespCode.Succeed.value
            resp['order'] = data
            resp['order']['sn'] = trans_id
            resp['order_items'] = OrderItemSerializer(order_item_qs).data
            resp['message'] = 'Success'
        transaction.set_autocommit(False)
        transaction.commit()
    except Exception as e:
        print(e)
        transaction.rollback()
        return RespCode.BusinessError.value, _('order submit error')
    return RespCode.Succeed.value, resp


def get_order_detail(request, sn):
    """ 订单支付页面 """
    # 当前用户
    v = VerifyUtil()
    user = v.verify_user(request=request)
    try:
        current_order_qs = Order.objects.filter(sn=sn, is_valid=True, user=user).first()
        order_item_qs = current_order_qs.order_item
        resp = {}
        data = OrderSerializer(current_order_qs).data
        resp['code'] = RespCode.Succeed.value
        resp['order'] = data
        resp['order']['sn'] = sn
        resp['order_items'] = OrderItemSerializer(order_item_qs).data
        resp['message'] = 'Success'
    except Exception as e:
        print(e)
        return RespCode.BusinessError.value, _('get order pay error')
    return RespCode.Succeed.value, resp


def order_pay_submit(request, sn):
    """
    1.选择支付方式
    2.数据验证
    3.调用支付宝接口支付
    4.改变订单状态，Order和OrderItem中的status
    5.增加Payment模型中的一条记录
    """
    # 先判断这个订单有没有被支付过
    v = VerifyUtil()
    user = v.verify_user(request=request)
    current_order = Order.objects.filter(sn=sn, is_valid=True, user=user).first()
    # 订单状态为已支付时
    if current_order.status == OrderStatus.PAID:
        return RespCode.BusinessError.value, _('user already paid this order')
    # 订单状态为待支付和已取消时:
    else:
        try:
            with transaction.atomic():
                current_order.status = OrderStatus.PAID
                current_order.order_item.status = OrderStatus.PAID
                current_order.save()
                current_order.order_item.save()
                Payment.objects.create(amount=current_order.buy_amount,
                                       pay_sn=sn,
                                       third_sn=Generate().get_trans_id(third=True),
                                       status=PayStatus.PAID,
                                       user=user, order=current_order)
            transaction.set_autocommit(False)
            transaction.commit()
            resp = {
                'code': RespCode.Succeed.value,
                'message': 'pay success'
            }
        except Exception as e:
            print(e)
            transaction.rollback()
            return RespCode.BusinessError.value, _('pay order error, please check')
    return RespCode.Succeed.value, resp


def order_cancel(request, sn):
    """ 取消订单 """
    v = VerifyUtil()
    user = v.verify_user(request=request)
    current_order = Order.objects.filter(sn=sn, is_valid=True, user=user).first()
    if current_order.status == OrderStatus.CANCELED:
        return RespCode.BusinessError.value, _('user already canceled this order')
    elif current_order.status == OrderStatus.SUBMIT:
        # 只能在订单状态为待支付时才能取消订单
        try:
            with transaction.atomic():
                current_order.status = OrderStatus.CANCELED
                current_order.order_item.status = OrderStatus.CANCELED
                current_order.save()
                current_order.order_item.save()
                # 库存回到原来数量
                order_item = current_order.order_item
                # content_object:自动帮忙找到对应的对象
                sight_ticket_obj = order_item.content_object
                sight_ticket_obj.remain_stock = F('remain_stock') + current_order.buy_count
                sight_ticket_obj.save()
            transaction.set_autocommit(False)
            transaction.commit()
        except Exception as e:
            print(e)
            transaction.rollback()
            return RespCode.BusinessError.value, _('pay order error, please check')
    else:
        return RespCode.BusinessError.value, _('user already paid this order')
    return RespCode.Succeed.value, _('pay cancel')


def order_delete(request, sn):
    """ 删除订单 """
    v = VerifyUtil()
    user = v.verify_user(request=request)
    current_order = Order.objects.filter(sn=sn, user=user).first()
    if current_order.is_valid is False:
        return RespCode.BusinessError.value, _('this order has already deleted')
    else:
        # 只能订单状态为已取消或已支付状态才能删除
        if current_order.status == OrderStatus.SUBMIT:
            # 订单状态为待支付时
            return RespCode.BusinessError.value, _('order status submit not allow delete')
        else:
            try:
                with transaction.atomic():
                    current_order.is_valid = False
                    current_order.order_item.is_valid = False
                    current_order.save()
                    current_order.order_item.save()
                transaction.set_autocommit(False)
                transaction.commit()
            except Exception as e:
                print(e)
                transaction.rollback()
                return RespCode.BusinessError.value, _('delete order error, please check')
    return RespCode.Succeed.value, _('order deleted success')


def get_my_orders(request, status, current_page, limit):
    """ 获取我的订单列表 """
    meta = {}
    v = VerifyUtil()
    user = v.verify_user(request=request)
    try:
        if status == 0:
            # 显示全部订单
            order_list = Order.objects.filter(is_valid=True, user=user).all()
            paginator = Paginator(order_list, limit)
            page_data = paginator.page(current_page)
            objects = OrderDetailSerializer(page_data, many=True).data
            meta['current_page'] = current_page
            meta['page_count'] = paginator.num_pages
            meta['total_count'] = paginator.count
            return RespCode.Succeed.value, meta, objects
        elif status in [OrderStatus.PAID, OrderStatus.SUBMIT, OrderStatus.CANCELED]:
            order_list = Order.objects.filter(is_valid=True, user=user, status=status).all()
            paginator = Paginator(order_list, limit)
            page_data = paginator.page(current_page)
            objects = OrderDetailSerializer(page_data, many=True).data
            meta['current_page'] = current_page
            meta['page_count'] = paginator.num_pages
            meta['total_count'] = paginator.count
            return RespCode.Succeed.value, meta, objects
        else:
            return RespCode.BusinessError.value, {}, _('order status error, please check')
    except Exception as e:
        print(e)
        return RespCode.BusinessError.value, {}, _('get order list failed')
