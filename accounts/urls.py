from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from accounts import views

urlpatterns = [
    # 用户列表接口
    path('user/list/', views.GetUserListView.as_view(), name='user_list'),
    # 用户信息接口
    path('user/info/', views.GetUserInfoView.as_view(), name='user_info'),
    # 邮箱验证码
    path('sendcode/email/', views.SendEmailCodeView.as_view()),
    # 手机验证码
    path('sendcode/phone/', views.SendPhoneCodeView.as_view()),
    # 注册接口
    path('register/', views.RegisterView.as_view(), name='register'),
    # 登录接口
    path('login/', views.LoginView.as_view(), name='login'),
    # 刷新token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
