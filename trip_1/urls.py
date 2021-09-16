from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include, re_path
from django.views.static import serve
from rest_framework_simplejwt.views import TokenRefreshView
from trip_1 import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # 系统模块
    path('system/', include('system.urls')),
    # 景点模块
    path('sight/', include('sight.urls')),
    # 用户模块
    path('accounts/', include('accounts.urls')),
    # 订单模块
    path('order/', include('order.urls')),
    # 后端统计报表
    path('master/', include('master.urls')),
    # 配合MEDIA_ROOT，可以在浏览器的地址栏访问media文件夹及里面的文件
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)/$', serve, {'document_root': settings.STATIC_ROOT}),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
# 该助手函数只能在 debug 模式下生效，且要求前缀是本地的（例如 /static/）
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
