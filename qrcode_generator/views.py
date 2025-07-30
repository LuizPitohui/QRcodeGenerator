
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
from django.views.generic.edit import DeleteView

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
    
    # Este decorador é necessário porque o seu JS envia JSON,
    # o que não inclui o token CSRF da mesma forma que um formulário padrão.
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request):
        try:
            # ✅ CORREÇÃO: Volte a ler os dados como JSON a partir do corpo da requisição.
            data = json.loads(request.body)
            title = data.get('title', '').strip()
            content = data.get('content', '').strip()
            qr_type = data.get('type', 'text')
            size = int(data.get('size', 10))
            border = int(data.get('border', 4))
            
            if not content:
                return JsonResponse({'success': False, 'error': 'Conteúdo não pode estar vazio'})

            # Agora a variável 'title' terá o valor correto vindo do JSON.
            history_entry = QRCodeHistory.objects.create(
                user=request.user if request.user.is_authenticated else None,
                title=title if title else f"QR Code para {qr_type}",
                content=content,
                qr_type=qr_type,
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )

            # O resto da sua lógica para gerar a imagem e retornar a resposta está perfeito.
            redirect_url = request.build_absolute_uri(
                reverse('qr_redirect', kwargs={'pk': history_entry.pk})
            )
            qr = qrcode.QRCode(
                version=1, 
                error_correction=qrcode.constants.ERROR_CORRECT_L, 
                box_size=size, 
                border=border
            )
            qr.add_data(redirect_url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue()).decode()

            history_entry.qr_code_image = img_str
            history_entry.save()
            
            return JsonResponse({
                'success': True, 
                'image': f'data:image/png;base64,{img_str}', 
                'content': content,
                'title': history_entry.title
            })
            
        except Exception as e:
            print(f"Erro em GenerateQRCodeView: {e}") 
            return JsonResponse({'success': False, 'error': f'Erro interno ao gerar QR Code: {str(e)}'})

# ✅ NOVA VIEW PARA REDIRECIONAMENTO
class QRRedirectView(View):
    """Busca o QR Code pelo ID e redireciona para o conteúdo final."""
    def get(self, request, pk):
        qr_code = get_object_or_404(QRCodeHistory, pk=pk)
        # Simplesmente redireciona para o conteúdo armazenado (ex: a URL do PDF)
        return redirect(qr_code.content)

# ✅ NOVA VIEW PARA EDIÇÃO
class EditQRCodeView(LoginRequiredMixin, View):
    template_name = 'qrcode_generator/edit_qrcode.html'
    form_class = QREditForm

    def get(self, request, pk):
        # Garante que o usuário só possa editar seus próprios QR Codes
        qr_instance = get_object_or_404(QRCodeHistory, pk=pk, user=request.user)
        form = self.form_class(instance=qr_instance)
        return render(request, self.template_name, {'form': form, 'qr_instance': qr_instance})

    def post(self, request, pk):
        # Garante que o usuário só possa editar seus próprios QR Codes
        qr_instance = get_object_or_404(QRCodeHistory, pk=pk, user=request.user)
        form = self.form_class(request.POST, request.FILES, instance=qr_instance)

        if form.is_valid():
            instance = form.save(commit=False)
            selected_type = form.cleaned_data['qr_type']
            
            if selected_type == 'pdf':
                new_pdf = form.cleaned_data.get('new_pdf_file')
                if new_pdf:
                    pdf_instance = PdfFile.objects.create(title=new_pdf.name, pdf_file=new_pdf)
                    instance.content = request.build_absolute_uri(pdf_instance.pdf_file.url)
            
            instance.qr_type = selected_type
            instance.save() # O campo 'title' será salvo aqui junto com o resto
            
            return redirect('history')
        
        return render(request, self.template_name, {'form': form, 'qr_instance': qr_instance})
    
# ... (HistoryView, DownloadQRCodeView, UploadPDFView permanecem os mesmos) ...
# ✅ MODIFICAÇÃO PRINCIPAL NA HISTORYVIEW
class HistoryView(LoginRequiredMixin, View): # 1. Herde de LoginRequiredMixin
    """View para exibir histórico de QR Codes do usuário logado."""
    login_url = reverse_lazy('login') # Redireciona para o login se não estiver autenticado

    def get(self, request):
        """Exibe o histórico paginado filtrado por usuário."""
        
        # 2. Filtra os resultados para pegar apenas os do usuário logado
        history_list = QRCodeHistory.objects.filter(user=request.user).order_by('-created_at')
        
        # ✅ 2. CRIE UM DICIONÁRIO COM OS TIPOS DE QR CODE PARA USAR NO FILTRO
        qr_code_types = QRCodeHistory.QRCODE_TYPES
        
        paginator = Paginator(history_list, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        return render(request, 'qrcode_generator/history.html', {
            'page_obj': page_obj,
            'history_list': history_list,
            'qr_code_types': qr_code_types
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


# ✅ NOVA VIEW PARA EXCLUSÃO
class DeleteQRCodeView(LoginRequiredMixin, DeleteView):
    """
    View para excluir um QR Code.
    - Herda de LoginRequiredMixin para garantir que o usuário esteja logado.
    - Herda de DeleteView para simplificar a lógica de exclusão.
    """
    model = QRCodeHistory
    # Define o template que pedirá a confirmação da exclusão.
    template_name = 'qrcode_generator/confirm_delete.html'
    # Para onde o usuário será redirecionado após a exclusão bem-sucedida.
    success_url = reverse_lazy('history')
    # Nome do objeto no contexto do template (ex: `{{ qrcode }}`).
    context_object_name = 'qrcode'

    def get_queryset(self):
        """
        Sobrescreve o método padrão para garantir que um usuário
        só possa excluir os QR codes que ele mesmo criou.
        Esta é uma medida de segurança CRUCIAL.
        """
        # Pega o queryset original
        qs = super().get_queryset()
        # Filtra para retornar apenas os registros pertencentes ao usuário logado
        return qs.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        """Adiciona dados extras ao contexto do template."""
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Confirmar Exclusão'
        return context
