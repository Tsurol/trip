from django.urls import path
from sight import views

urlpatterns = [
    # 景点列表接口
    path('sight/list/', views.GetSightView.as_view(), name='sight_list'),
    path('sight/list/cache', views.GetSightCacheView.as_view(), name='sight_list_cache'),
    # 景点详情信息接口,pk为sight.id
    path('sight/detail/<int:pk>/', views.GetSightDetail.as_view(), name='sight_detail'),
    # 景点下的评论接口
    path('comment/list/<int:pk>/', views.GetCommentView.as_view(), name='sight_comment_list'),
    # 景点下的门票接口
    path('ticket/list/<int:pk>/', views.GetTicketView.as_view(), name='sight_ticket_list'),
    # 景点介绍接口
    path('sight/info/<int:pk>/', views.GetSightInfoView.as_view(), name='sight_info'),
    # 景点门票详情信息接口
    path('ticket/detail/<int:pk>/', views.GetTicketDetailView.as_view(), name='ticket_detail'),
    # 景点下的图片接口
    path('image/list/<int:pk>/', views.GetImageListView.as_view(), name='image_list'),
]
