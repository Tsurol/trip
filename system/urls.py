from django.urls import path

from system import views

urlpatterns = [
    path('slider/list/', views.GetSliderView.as_view(), name='GetSliderView'),
]

