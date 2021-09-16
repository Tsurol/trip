from django.core.paginator import Paginator
from django.db.models import Q

from trip_1.enums import RespCode
from system.models import Slider
from system.serializers import SliderSerializer


def get_slider_list(types, current_page, page_size):
    meta = {}
    objects = []
    try:
        query = Q(is_valid=True)
        query = query & Q(types=types)
        qs = Slider.objects.filter(query)
        if not qs:
            return RespCode.NotFound.value, {}, []
        paginator = Paginator(qs, page_size)
        page_data = paginator.page(current_page)
        objects = SliderSerializer(page_data, many=True).data
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
