# coding:utf-8
from trip_1.serializers import CustomFieldsSerializer
from system.models import Slider, ImageRelated


class SliderSerializer(CustomFieldsSerializer):
    """ 轮播图序列化 """
    class Meta:
        model = Slider
        fields = ('id', 'name', 'img', 'target_url', 'types')
