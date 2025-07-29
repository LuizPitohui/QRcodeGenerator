# qrcode_generator/models.py
from django.db import models
from django.utils import timezone

class QRCodeHistory(models.Model):
    # ... (seu código existente) ...
    QRCODE_TYPES = [
        ('text', 'Texto'),
        ('url', 'URL'),
        ('pdf', 'PDF'),
        ('email', 'Email'),
        ('phone', 'Telefone'),
        ('sms', 'SMS'),
        ('wifi', 'WiFi'),
        ('vcard', 'vCard'),
    ]

    content = models.TextField(verbose_name='Conteúdo')
    qr_type = models.CharField(max_length=10, choices=QRCODE_TYPES, default='text', verbose_name='Tipo')
    
    # ✅ NOVO CAMPO PARA ARMAZENAR A IMAGEM
    qr_code_image = models.TextField(blank=True, verbose_name='Imagem do QR Code (Base64)')

    created_at = models.DateTimeField(default=timezone.now, verbose_name='Criado em')
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name='IP')
    user_agent = models.TextField(blank=True, verbose_name='User Agent')
    
    class Meta:
        verbose_name = 'Histórico de QR Code'
        verbose_name_plural = 'Histórico de QR Codes'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.get_qr_type_display()} - {self.content[:50]}...'

# O modelo PdfFile permanece o mesmo
class PdfFile(models.Model):
    title = models.CharField(max_length=200)
    pdf_file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
