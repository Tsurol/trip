from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.utils.translation import ugettext_lazy as _
from trip_1.enums import RespCode
from utils.response import reformat_resp, error_resp
from system.business import get_slider_list
from system.models import Slider
from django.db.models import Q


class GetSliderView(APIView):
    """ 轮播图接口 """
    permission_classes = [AllowAny]

    def get(self, request):
        types = request.query_params.get('types', 10)
        # 当前页码
        current_page = int(request.query_params.get('page', 1))
        code, meta, objects = get_slider_list(types, current_page, page_size=5)
        if code == RespCode.Succeed.value:
            return reformat_resp(code, meta, objects, 'Succeed')
        elif code == RespCode.NotFound.value:
            return error_resp(code, _('Resource not found'))
        else:
            return error_resp(code, _('Server exception, please try again'))
