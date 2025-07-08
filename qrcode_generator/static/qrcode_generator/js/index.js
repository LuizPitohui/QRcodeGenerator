// static/qrcode_generator/js/index.js

document.addEventListener("DOMContentLoaded", function() {
    
    // ✅ 1. PRIMEIRO MARCADOR
    console.log("Script iniciado: DOMContentLoaded foi disparado.");

    // --- ELEMENTOS DO FORMULÁRIO PRINCIPAL ---
    const mainForm = document.getElementById("qrForm");
    
    // ✅ 2. SEGUNDO MARCADOR (E um erro mais claro)
    console.log("Procurando o formulário principal. Encontrado:", mainForm);
    if (!mainForm) { 
        console.error("ERRO CRÍTICO: Formulário com id='qrForm' não foi encontrado. O script será interrompido.");
        return; 
    }
    
    const qrTypeSelect = document.getElementById("qrType");
    const qrContentInput = document.getElementById("qrContent");
    const generateBtn = document.getElementById("generateBtn");
    const loadingSpinner = document.querySelector(".loading-spinner");
    const alertContainer = document.getElementById("alertContainer");
    const qrResult = document.getElementById("qrResult");
    const qrImage = document.getElementById("qrImage");
    const qrContentDisplay = document.getElementById("qrContentDisplay");

    // --- ELEMENTOS DO MODAL DE UPLOAD ---
    const pdfUploadModalElement = document.getElementById('pdfUploadModal');
    const pdfUploadModal = new bootstrap.Modal(pdfUploadModalElement);
    const pdfUploadForm = document.getElementById('pdfUploadForm');
    const uploadPdfBtn = document.getElementById('uploadPdfBtn');
    const pdfUploadSpinner = document.getElementById('pdfUploadSpinner');
    
    const generateUrl = mainForm.dataset.generateUrl;
    const uploadPdfUrl = mainForm.dataset.uploadPdfUrl;
    let previousQrType = qrTypeSelect.value;

    // --- LÓGICA PARA ABRIR O MODAL ---
    qrTypeSelect.addEventListener('change', function() {
        if (this.value === 'pdf') {
            pdfUploadModal.show();
            this.value = previousQrType;
        } else {
            previousQrType = this.value;
        }
    });

    // --- LÓGICA PARA FAZER O UPLOAD DO PDF ---
    uploadPdfBtn.addEventListener('click', function() {
        if (!pdfUploadForm.checkValidity()) {
            pdfUploadForm.reportValidity();
            return;
        }
        const formData = new FormData(pdfUploadForm);
        uploadPdfBtn.disabled = true;
        pdfUploadSpinner.classList.remove('d-none');

        fetch(uploadPdfUrl, { 
            method: 'POST',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                pdfUploadModal.hide();
                qrContentInput.value = data.url;
                qrTypeSelect.value = 'url';
                showAlert("Upload do PDF realizado com sucesso! Agora gere o QR Code.", "success");
            } else {
                alert('Erro no upload: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Erro no fetch do upload:', error);
            alert('Ocorreu um erro de conexão. Tente novamente.');
        })
        .finally(() => {
            uploadPdfBtn.disabled = false;
            pdfUploadSpinner.classList.add('d-none');
            pdfUploadForm.reset();
        });
    });

    // ✅ 3. TERCEIRO MARCADOR
    console.log("Anexando a lógica ao botão 'Gerar QR Code'...");

    // --- LÓGICA PARA GERAR O QR CODE (FORMULÁRIO PRINCIPAL) ---
    mainForm.addEventListener('submit', function(e) {
        // ✅ 4. MARCADOR DE EXECUÇÃO
        console.log("Botão 'Gerar QR Code' clicado, prevenindo envio padrão.");
        e.preventDefault();
        
        const formData = new FormData(mainForm);
        const data = {
            content: formData.get("content"),
            type: formData.get("type"),
            size: formData.get("size"),
            border: formData.get("border")
        };

        generateBtn.disabled = true;
        loadingSpinner.classList.add("show");
        hideAlert();
        qrResult.classList.remove("show");

        fetch(generateUrl, {
            method: "POST",
            headers: { "Content-Type": "application/json", 'X-CSRFToken': getCookie('csrftoken') },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                qrImage.src = data.image;
                qrContentDisplay.textContent = data.content;
                qrResult.classList.add("show");
                showAlert("QR Code gerado com sucesso!", "success");
            } else {
                showAlert(data.error || "Ocorreu um erro desconhecido", "danger");
            }
        })
        .catch(error => {
            console.error("Erro na requisição:", error);
            showAlert("Erro de conexão. Verifique o console para mais detalhes.", "danger");
        })
        .finally(() => {
            generateBtn.disabled = false;
            loadingSpinner.classList.remove("show");
        });
    });

    console.log("Configuração de eventos do script index.js concluída.");

    // --- FUNÇÕES AUXILIARES ---
    function getCookie(name) {
        // ... (código da função)
    }

    function showAlert(message, type) {
        // ... (código da função)
    }

    function hideAlert() {
        // ... (código da função)
    }
});