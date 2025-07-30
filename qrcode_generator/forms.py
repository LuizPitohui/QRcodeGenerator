# qrcode_generator/forms.py

from django import forms
from .models import PdfFile, QRCodeHistory

class PdfUploadForm(forms.ModelForm):
    class Meta:
        model = PdfFile
        fields = ['title', 'pdf_file']
        labels = {
            'title': 'Título do Arquivo',
            'pdf_file': 'Selecione o PDF'
        }

# ✅ FORMULÁRIO DE EDIÇÃO ATUALIZADO E CORRIGIDO
class QREditForm(forms.ModelForm):
    # Definimos o campo 'qr_type' explicitamente para ter mais controle
    qr_type = forms.ChoiceField(
        choices=QRCodeHistory.QRCODE_TYPES,
        label="Tipo de QR Code",
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_qr_type_edit'})
    )

    # Campo para upload de um novo PDF, não obrigatório
    new_pdf_file = forms.FileField(
        required=False,
        label="Substituir Arquivo PDF",
        help_text="Selecione um novo arquivo apenas se desejar substituir o PDF atual.",
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = QRCodeHistory
        # ✅ 1. ADICIONE O CAMPO 'title' À LISTA DE CAMPOS
        fields = ['title', 'qr_type', 'content']
        labels = {
            # ✅ 2. ADICIONE UM LABEL PARA O TÍTULO
            'title': 'Título',
            'content': 'Conteúdo (Texto, URL, etc.)',
        }
        widgets = {
            # ✅ 3. APLIQUE ESTILOS CSS AO CAMPO DE TÍTULO
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
