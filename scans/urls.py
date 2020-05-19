from django.urls import path
from . import views


app_name = 'scans'
urlpatterns = [
    path('', views.index, name='index'),
    path('history/<int:scan_id>/', views.detail, name='detail'),
    path('new/', views.new, name='new'),
    path('devices/', views.devices, name='devices'),
]