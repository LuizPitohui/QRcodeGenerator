from django.db import models
from django.utils import timezone
# ✅ 1. Importe o modelo de usuário padrão do Django
from django.contrib.auth.models import User

class QRCodeHistory(models.Model):
    # ✅ 2. Adicione um campo para relacionar o QR Code ao usuário
    #    - `ForeignKey` cria a relação.
    #    - `on_delete=models.CASCADE` significa que se o usuário for deletado, seus QR codes também serão.
    #    - `null=True, blank=True` permite que QR codes antigos (sem usuário) não quebrem o sistema.
    #      Para novos projetos, você pode remover `null=True, blank=True` e tornar o campo obrigatório.
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário', null=True, blank=True)
    title = models.CharField(max_length=200, verbose_name='Título', blank=True, default='QR Code sem título')
    # ... (o resto do seu modelo permanece igual) ...
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
    qr_code_image = models.TextField(blank=True, verbose_name='Imagem do QR Code (Base64)')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Criado em')
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name='IP')
    user_agent = models.TextField(blank=True, verbose_name='User Agent')

    class Meta:
        verbose_name = 'Histórico de QR Code'
        verbose_name_plural = 'Histórico de QR Codes'
        ordering = ['-created_at']

    def __str__(self):
        # É uma boa prática incluir o usuário na representação em texto
        user_info = self.user.username if self.user else 'Anônimo'
        return f'{self.get_qr_type_display()} por {user_info} - {self.content[:40]}...'

# O modelo PdfFile permanece o mesmo
class PdfFile(models.Model):
    title = models.CharField(max_length=200)
    pdf_file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
