
import qrcode
import io
import base64
import json
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

# ✅ IMPORTS QUE FALTAVAM OU PRECISAM ESTAR PRESENTES
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .forms import PdfUploadForm, QREditForm
from .models import QRCodeHistory, PdfFile
# ... (MyLoginView, HomeView, get_client_ip) ...

class MyLoginView(LoginView):
    """View para autenticação de usuários."""
    template_name = 'qrcode_generator/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        """Define a URL de redirecionamento após o login bem-sucedido."""
        # CORRETO: Use o nome da URL definido em urls.py
        return reverse_lazy('home')
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

class GenerateQRCodeView(View):
    """View para gerar QR Codes dinâmicos."""
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            content = data.get('content', '').strip()
            qr_type = data.get('type', 'text')
            size = int(data.get('size', 10))
            border = int(data.get('border', 4))
            
            if not content:
                return JsonResponse({'success': False, 'error': 'Conteúdo não pode estar vazio'})

            # 1. Salva o registro no banco PRIMEIRO para obter um ID
            history_entry = QRCodeHistory.objects.create(
                content=content, # Salva o conteúdo final (ex: a URL do PDF)
                qr_type=qr_type,
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )

            # 2. Cria a URL de redirecionamento usando o ID do objeto salvo
            # Ex: https://meusite.com/redirect/123/
            redirect_url = request.build_absolute_uri(
                reverse('qr_redirect', kwargs={'pk': history_entry.pk} )
            )

            # 3. Gera a imagem do QR Code usando a URL de REDIRECIONAMENTO
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=size, border=border)
            qr.add_data(redirect_url) # A MÁGICA ACONTECE AQUI!
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue()).decode()

            # 4. Salva a imagem gerada no registro do banco
            history_entry.qr_code_image = img_str
            history_entry.save()
            
            # 5. Retorna a imagem e o conteúdo para o front-end
            return JsonResponse({
                'success': True, 
                'image': f'data:image/png;base64,{img_str}', 
                'content': content # Mostra o conteúdo original para o usuário
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Erro ao gerar QR Code: {str(e)}'})

# ✅ NOVA VIEW PARA REDIRECIONAMENTO
class QRRedirectView(View):
    """Busca o QR Code pelo ID e redireciona para o conteúdo final."""
    def get(self, request, pk):
        qr_code = get_object_or_404(QRCodeHistory, pk=pk)
        # Simplesmente redireciona para o conteúdo armazenado (ex: a URL do PDF)
        return redirect(qr_code.content)

# ✅ NOVA VIEW PARA EDIÇÃO
class EditQRCodeView(LoginRequiredMixin, View):
    """View para editar o tipo e o conteúdo de um QR Code existente."""
    template_name = 'qrcode_generator/edit_qrcode.html'
    form_class = QREditForm

    def get(self, request, pk):
        qr_instance = get_object_or_404(QRCodeHistory, pk=pk)
        form = self.form_class(instance=qr_instance)
        return render(request, self.template_name, {'form': form, 'qr_instance': qr_instance})

    def post(self, request, pk):
        qr_instance = get_object_or_404(QRCodeHistory, pk=pk)
        form = self.form_class(request.POST, request.FILES, instance=qr_instance)

        if form.is_valid():
            # Pega a instância do formulário, mas não salva no banco ainda (commit=False)
            # Isso nos permite modificar os dados antes de salvar.
            instance = form.save(commit=False)

            # Pega o tipo de QR Code selecionado no formulário
            selected_type = form.cleaned_data['qr_type']
            
            # LÓGICA CONDICIONAL: Se o tipo for PDF, o conteúdo DEVE ser uma URL de arquivo.
            if selected_type == 'pdf':
                new_pdf = request.FILES.get('new_pdf_file')
                if new_pdf:
                    # Se um novo PDF foi enviado, salva-o e atualiza o conteúdo.
                    pdf_instance = PdfFile.objects.create(title=new_pdf.name, pdf_file=new_pdf)
                    instance.content = request.build_absolute_uri(pdf_instance.pdf_file.url)
                # Se não enviou um novo PDF, o conteúdo antigo (URL do PDF anterior) é mantido.
                # Não fazemos nada aqui, pois o form.save() cuidará disso.
            
            # Garante que o tipo seja salvo corretamente
            instance.qr_type = selected_type
            
            # Agora, salva a instância com todas as modificações
            instance.save()
            
            return redirect('history')
        
        # Se o formulário for inválido, renderiza a página novamente com os erros
        return render(request, self.template_name, {'form': form, 'qr_instance': qr_instance})
    
# ... (HistoryView, DownloadQRCodeView, UploadPDFView permanecem os mesmos) ...
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