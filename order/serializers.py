# coding:utf-8
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from order.models import Order, OrderItem
from trip_1.serializers import CustomFieldsSerializer


class OrderItemSerializer(CustomFieldsSerializer):
    """ 订单明细序列化 """
    app_label = serializers.SerializerMethodField(label=_('app label'), read_only=True)
    model = serializers.SerializerMethodField(label=_('model'), read_only=True)

    class Meta:
        model = OrderItem
        fields = (
            'id', 'buy_amount', 'app_label', 'model', 'object_id', 'buy_count', 'flash_discount', 'flash_img',
            'flash_name',
            'flash_origin_price', 'flash_price', 'remark')

    def get_app_label(self, obj):
        if obj.is_valid:
            app_label = obj.content_type.app_label
            return app_label
        else:
            return False

    def get_model(self, obj):
        if obj.is_valid:
            model = obj.content_type.model
            return model
        else:
            return False


class OrderSerializer(CustomFieldsSerializer):
    """ 门票订单序列化 """
    created_at = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'sn', 'buy_amount', 'buy_count', 'created_at', 'express_no', 'express_type',
                  'remark', 'status', 'to_address', 'to_area', 'to_phone', 'to_user', 'types')

    def get_created_at(self, obj):
        """ 获取评论的创建时间-年月日 """
        return obj.created_at.strftime('%Y-%m-%d %H-%M-%S')


class OrderDetailSerializer(CustomFieldsSerializer):
    """ 门票订单序列化 """
    sight_id = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.SerializerMethodField(read_only=True)
    order_item = OrderItemSerializer()

    class Meta:
        model = Order
        fields = ('id', 'sn', 'buy_amount', 'buy_count', 'created_at', 'express_no', 'express_type',
                  'remark', 'status', 'to_address', 'to_area', 'to_phone', 'to_user', 'sight_id', 'types', 'order_item')

    def get_created_at(self, obj):
        """ 获取评论的创建时间-年月日 """
        return obj.created_at.strftime('%Y-%m-%d %H-%M-%S')

    def get_sight_id(self, obj):
        """ 获取景点id """
        return obj.order_item.content_object.sight.id
