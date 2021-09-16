from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

from accounts.serializers import UserSerializer
from system.models import ImageRelated
from trip_1.serializers import CustomFieldsSerializer
from sight.models import Sight, Comment, SightTicket, SightInfo


class SightSerializer(CustomFieldsSerializer):
    """ 景点列表序列化 """
    # drf模型序列化器默认仅返回数据库中已存在字段,新增数据库不存在的字段
    comment_count = serializers.SerializerMethodField(label=_('comment_count of sight'), read_only=True)

    class Meta:
        model = Sight
        fields = ('id', 'name', 'main_img', 'score', 'province', 'city', 'min_price', 'comment_count')

    def get_comment_count(self, obj):
        """ 获取景点下的评论数量 """
        # obj是Sight模型实例对象
        comment_count = obj.comments.filter(is_valid=True).count()
        return comment_count


class SightDetailSerializer(CustomFieldsSerializer):
    """ 景点详情信息序列化 """
    images = serializers.SerializerMethodField(label=_('images of sight'), read_only=True)
    comment_count = serializers.SerializerMethodField(label=_('comment_count of sight'), read_only=True)
    image_count = serializers.SerializerMethodField(label=_('image count of sight'), read_only=True)
    full_address = serializers.SerializerMethodField(label=_('full address'), read_only=True)

    class Meta:
        model = Sight
        fields = ('id', 'name', 'area', 'city', 'content',
                  'min_price', 'province', 'score', 'town',
                  'desc', 'main_img', 'banner_img', 'images', 'comment_count', 'full_address', 'image_count')

    def get_images(self, obj):
        """ 获取景点下的图片信息 """
        images = obj.images.filter(is_valid=True)
        images_list = []
        for image in images:
            images_list.append({
                'img': image.img.url,
                'summary': image.summary
            })
        return images_list

    def get_comment_count(self, obj):
        """ 获取景点下的评论数量 """
        # obj是Sight模型实例对象
        comment_count = obj.comments.filter(is_valid=True).count()
        return comment_count

    def get_image_count(self, obj):
        """ 获取景点下的图片数量 """
        image_count = obj.images.filter(is_valid=True).count()
        return image_count

    def get_full_address(self, obj):
        """ 获取景点的完整地址 """
        # area和town可能为空
        if obj.area and obj.town:
            full_address = obj.province + obj.city + obj.area + obj.town
            return full_address
        elif obj.area or obj.town:
            if obj.area:
                full_address = obj.province + obj.city + obj.area
                return full_address
            elif obj.town:
                full_address = obj.province + obj.city + obj.town
                return full_address
        else:
            full_address = obj.province + obj.city
            return full_address


class CommentSerializer(CustomFieldsSerializer):
    """ 景点评论列表序列化 """
    # 外键的序列化
    images = serializers.SerializerMethodField(label=_('images of comment'), read_only=True)
    created_at = serializers.SerializerMethodField(label=_('comment created at'), read_only=True)
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'content', 'is_top', 'love_count', 'score', 'user', 'created_at', 'is_public', 'images')

    def get_created_at(self, obj):
        """ 获取评论的创建时间-年月日 """
        return obj.created_at.strftime('%Y-%m-%d')

    def get_images(self, obj):
        """ 获取评论中的图片 """
        # ImageRelated对象
        images = obj.images.filter(is_valid=True)
        images_list = []
        for image in images:
            images_list.append({
                'id': image.id,
                'img': image.img.url,
                'summary': image.summary
            })
        return images_list


class TicketSerializer(CustomFieldsSerializer):
    """ 景点门票列表序列化 """
    entry_way = serializers.SerializerMethodField(label=_('entry way'), read_only=True)

    class Meta:
        model = SightTicket
        fields = ('id', 'name', 'desc', 'types', 'price',
                  'sell_price', 'discount', 'total_stock', 'remain_stock', 'entry_way')

    def get_entry_way(self, obj):
        if obj.entry_way == 0:
            obj.entry_way = '短信换票入园'
        else:
            obj.entry_way = '凭借验证码入园'
        return obj.entry_way


class SightInfoSerializer(CustomFieldsSerializer):
    """ 景点介绍序列化 """

    class Meta:
        model = SightInfo
        fields = ('id', 'entry_explain', 'play_way', 'tips', 'traffic')


class TicketDetailSerializer(CustomFieldsSerializer):
    """ 景点门票详情信息序列化 """
    entry_way = serializers.SerializerMethodField(label=_('entry way'), read_only=True)

    class Meta:
        model = SightTicket
        fields = ('id', 'name', 'desc', 'types', 'price', 'sell_price', 'discount', 'tips',
                  'expire_date', 'return_policy', 'has_invoice', 'entry_way', 'remark')

    def get_entry_way(self, obj):
        if obj.entry_way == 0:
            obj.entry_way = '短信换票入园'
        else:
            obj.entry_way = '凭借验证码入园'
        return obj.entry_way


class SightImageSerializer(CustomFieldsSerializer):
    """ 景点下的图片序列化 """

    class Meta:
        model = ImageRelated
        fields = ('id', 'img', 'summary')
