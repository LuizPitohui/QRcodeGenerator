# qrcode_generator/models.py
from django.db import models
from django.utils import timezone

class QRCodeHistory(models.Model):
    """
    Modelo para armazenar o histórico de QR Codes gerados
    """
    QRCODE_TYPES = [
        ('text', 'Texto'),
        ('url', 'URL'),
        ('pdf', 'PDF'), # ✅ ADICIONE ESTA OPÇÃO
        ('email', 'Email'),
        ('phone', 'Telefone'),
        ('sms', 'SMS'),
        ('wifi', 'WiFi'),
        ('vcard', 'vCard'),
    ]

    # Adicionando as opções de expiração
    EXPIRATION_TYPES = [
        ('never', 'Nunca Expira'),
    ]

    content = models.TextField(verbose_name='Conteúdo')
    qr_type = models.CharField(
        max_length=10, 
        choices=QRCODE_TYPES, 
        default='text',
        verbose_name='Tipo'
    )

    created_at = models.DateTimeField(default=timezone.now, verbose_name='Criado em')
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name='IP')
    user_agent = models.TextField(blank=True, verbose_name='User Agent')
    
    class Meta:
        verbose_name = 'Histórico de QR Code'
        verbose_name_plural = 'Histórico de QR Codes'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.get_qr_type_display()} - {self.content[:50]}...'

class PdfFile(models.Model):
    title = models.CharField(max_length=200)
    pdf_file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title