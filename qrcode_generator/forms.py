# qrcode_generator/forms.py

from django import forms
from .models import PdfFile

class PdfUploadForm(forms.ModelForm):
    class Meta:
        model = PdfFile
        fields = ['title', 'pdf_file']
        labels = {
            'title': 'Título do Arquivo',
            'pdf_file': 'Selecione o PDF'
        }