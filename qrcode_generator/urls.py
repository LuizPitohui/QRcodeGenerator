from django.urls import path
from . import views

app_name = 'qrcode_generator'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('generate/', views.GenerateQRCodeView.as_view(), name='generate'),
    path('history/', views.HistoryView.as_view(), name='history'),
    path('download/', views.DownloadQRCodeView.as_view(), name='download'),
]

