from django.urls import path
from app import views
from app import magnitude
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.landing, name='landing'),
    path('city/', views.city_view, name='city_view'),
    path('magnitude/', views.get_magnitude, name='get_magnitude'),
    path('my_view/', views.my_view, name='my_view'),
    path('video/<str:video_id>/', views.video_player, name='video_player'),
]