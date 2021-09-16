from django.urls import path
from order import views

urlpatterns = [
    # 订单提交(post)
    path("order/ticket/submit/", views.OrderSubmitView.as_view()),
    # 订单支付页面(get)，立即支付(post)，取消订单(put)，删除订单(delete)
    path("order/detail/<int:sn>/", views.OrderDetailView.as_view()),
    # 我的订单列表
    path("order/list/", views.OrderListView.as_view()),
]
