import qrcode
import io
import base64
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.views import View
from .models import QRCodeHistory
from .forms import PdfUploadForm # ✅ IMPORTE O FORMULÁRIO

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin # Para proteger a HomeView
import json

# Sua view de login customizada (herdando da LoginView do Django)

class MyLoginView(LoginView):
    """View para autenticação de usuários."""
    template_name = 'qrcode_generator/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        """Define a URL de redirecionamento após o login bem-sucedido."""
        # CORRETO: Use o nome da URL definido em urls.py
        return reverse_lazy('home')

# Protegendo sua HomeView original
# Apenas usuários logados poderão acessá-la
class HomeView(LoginRequiredMixin, View):
    """View principal para geração de QR Codes"""
    login_url = reverse_lazy('login') # Para onde redirecionar se não estiver logado

    def get(self, request):
        """Renderiza a página principal"""
        return render(request, 'qrcode_generator/index.html')

def get_client_ip(request):
    """Obtém o IP real do cliente"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# qrcode_generator/views.py
# ... (imports e outras views) ...

class GenerateQRCodeView(View):
    """View para gerar QR Codes via AJAX"""
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request):
        """Gera QR Code baseado nos dados recebidos"""
        try:
            data = json.loads(request.body)
            content = data.get('content', '').strip()
            qr_type = data.get('type', 'text')
            size = int(data.get('size', 10))
            border = int(data.get('border', 4))
            
            
            if not content:
                return JsonResponse({'success': False, 'error': 'Conteúdo não pode estar vazio'})
            
            processed_content = self.process_content(content, qr_type)
            
            # ... (a lógica de geração do QR Code continua a mesma) ...
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=size, border=border)
            qr.add_data(processed_content)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            # ✅ BLOCO DE CRIAÇÃO MODIFICADO
            QRCodeHistory.objects.create(
                content=processed_content,
                qr_type=qr_type,
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            return JsonResponse({'success': True, 'image': f'data:image/png;base64,{img_str}', 'content': processed_content})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Erro ao gerar QR Code: {str(e)}'})

    # ... (o resto da view e do arquivo continua o mesmo) ...
    def process_content(self, content, qr_type):
        """Processa o conteúdo baseado no tipo de QR Code"""
        if qr_type == 'url':
            if not content.startswith(('http://', 'https://')):
                content = 'https://' + content
        elif qr_type == 'email':
            if not content.startswith('mailto:'):
                content = f'mailto:{content}'
        elif qr_type == 'phone':
            content = f'tel:{content}'
        elif qr_type == 'sms':
            content = f'sms:{content}'
        return content

# ... (outras views) ...


class HistoryView(View):
    """View para exibir histórico de QR Codes"""
    
    def get(self, request):
        """Exibe o histórico paginado"""
        history_list = QRCodeHistory.objects.all()
        paginator = Paginator(history_list, 20)  # 20 itens por página
        
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        return render(request, 'qrcode_generator/history.html', {
            'page_obj': page_obj
        })


class DownloadQRCodeView(View):
    """View para download de QR Code"""
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request):
        """Gera e retorna QR Code para download"""
        try:
            data = json.loads(request.body)
            content = data.get('content', '').strip()
            size = int(data.get('size', 10))
            border = int(data.get('border', 4))
            
            if not content:
                return HttpResponse('Conteúdo não pode estar vazio', status=400)
            
            # Gera o QR Code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=size,
                border=border,
            )
            qr.add_data(content)
            qr.make(fit=True)
            
            # Cria a imagem
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Retorna como download
            response = HttpResponse(content_type='image/png')
            response['Content-Disposition'] = 'attachment; filename="qrcode.png"'
            img.save(response, format='PNG')
            
            return response
            
        except Exception as e:
            return HttpResponse(f'Erro ao gerar QR Code: {str(e)}', status=500)

# ✅ ADICIONE ESTA NOVA VIEW
class UploadPDFView(View):
    """View para lidar com o upload de arquivos PDF via AJAX."""

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        # Usa o formulário para validar os dados recebidos (request.POST e request.FILES)
        form = PdfUploadForm(request.POST, request.FILES)

        if form.is_valid():
            # Salva o formulário, o que cria um novo objeto PdfFile no banco
            pdf_instance = form.save()
            
            # Constrói a URL completa para o arquivo salvo
            pdf_url = request.build_absolute_uri(pdf_instance.pdf_file.url)
            
            return JsonResponse({
                'success': True,
                'url': pdf_url, # Envia a URL de volta para o frontend
                'title': pdf_instance.title
            })
        else:
            # Se o formulário for inválido, retorna os erros
            return JsonResponse({
                'success': False,
                'error': 'Dados inválidos ou arquivo não enviado. Por favor, tente novamente.'
            })