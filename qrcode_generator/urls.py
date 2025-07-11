# qrcode_generator/urls.py

from django.urls import path
from . import views
from .views import HomeView, MyLoginView
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('', MyLoginView.as_view(), name='login'),
    path('home/', HomeView.as_view(), name='home'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('generate/', views.GenerateQRCodeView.as_view(), name='generate'),
    path('history/', views.HistoryView.as_view(), name='history'),
    path('download/', views.DownloadQRCodeView.as_view(), name='download'),
    path('upload-pdf/', views.UploadPDFView.as_view(), name='upload_pdf'),
]