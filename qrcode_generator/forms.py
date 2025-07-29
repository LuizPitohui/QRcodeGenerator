# qrcode_generator/forms.py

from django import forms
from .models import PdfFile, QRCodeHistory

class PdfUploadForm(forms.ModelForm):
    # ... (seu formulário existente) ...
    class Meta:
        model = PdfFile
        fields = ['title', 'pdf_file']
        labels = {
            'title': 'Título do Arquivo',
            'pdf_file': 'Selecione o PDF'
        }
# ✅ FORMULÁRIO DE EDIÇÃO CORRIGIDO
class QREditForm(forms.ModelForm):
    # Definimos o campo 'qr_type' explicitamente aqui
    # Usamos o choices diretamente do modelo para manter a consistência
    qr_type = forms.ChoiceField(
        choices=QRCodeHistory.QRCODE_TYPES,
        label="Tipo de QR Code",
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_qr_type_edit'}) # Adicionamos um ID explícito
    )

    # Campo para upload de um novo PDF, não obrigatório
    new_pdf_file = forms.FileField(
        required=False,
        label="Novo Arquivo PDF",
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = QRCodeHistory
        # 'qr_type' já foi definido acima, então o mantemos aqui para que o ModelForm saiba associá-lo
        fields = ['qr_type', 'content']
        labels = {
            'content': 'Conteúdo (Texto, URL, etc.)',
        }
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }