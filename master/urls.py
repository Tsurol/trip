from django.urls import path

from master import views

urlpatterns = [
    # echarts使用
    path('test/', views.test),
]
