# qrcode_generator/urls.py

from django.urls import path
from .views import (
    HomeView, 
    MyLoginView, 
    GenerateQRCodeView, 
    HistoryView, 
    DownloadQRCodeView, 
    UploadPDFView, 
    EditQRCodeView, 
    QRRedirectView
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # ✅ CORREÇÃO: Troque .views() por .as_view() em todas as linhas
    path('', MyLoginView.as_view(), name='login'),
    path('home/', HomeView.as_view(), name='home'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('generate/', GenerateQRCodeView.as_view(), name='generate'),
    path('history/', HistoryView.as_view(), name='history'),
    path('download/', DownloadQRCodeView.as_view(), name='download'),
    path('upload-pdf/', UploadPDFView.as_view(), name='upload_pdf'),
    path('edit/<int:pk>/', EditQRCodeView.as_view(), name='edit_qrcode'),
    path('redirect/<int:pk>/', QRRedirectView.as_view(), name='qr_redirect'),
]
