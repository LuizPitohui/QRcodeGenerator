// static/qrcode_generator/js/index.js

document.addEventListener("DOMContentLoaded", function () {

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
    const downloadBtn = document.getElementById("downloadBtn");

    // --- ELEMENTOS DO MODAL DE UPLOAD ---
    const pdfUploadModalElement = document.getElementById('pdfUploadModal');
    const pdfUploadModal = new bootstrap.Modal(pdfUploadModalElement);
    const pdfUploadForm = document.getElementById('pdfUploadForm');
    const uploadPdfBtn = document.getElementById('uploadPdfBtn');
    const pdfUploadSpinner = document.getElementById('pdfUploadSpinner');

    const generateUrl = mainForm.dataset.generateUrl;
    const uploadPdfUrl = mainForm.dataset.uploadPdfUrl;
    const downloadUrl = mainForm.dataset.downloadUrl;
    let previousQrType = qrTypeSelect.value;

    // --- LÓGICA PARA ABRIR O MODAL ---
    qrTypeSelect.addEventListener('change', function () {
        if (this.value === 'pdf') {
            pdfUploadModal.show();
            this.value = previousQrType;
        } else {
            previousQrType = this.value;
        }
    });

    // --- LÓGICA PARA FAZER O UPLOAD DO PDF ---
    uploadPdfBtn.addEventListener('click', function () {
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
    mainForm.addEventListener('submit', function (e) {
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
            headers: {
                "Content-Type": "application/json",
                'X-CSRFToken': getCookie('csrftoken')
            },
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

    // ✅ 4. LÓGICA PARA DOWNLOAD DO QR CODE
    downloadBtn.addEventListener('click', function () {
        const data = {
            content: document.getElementById("qrContentDisplay").textContent,
            size: document.getElementById("qrSize").value,
            border: document.getElementById("qrBorder").value
        };

        fetch(downloadUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(data)
        })
            .then(response => {
                if (response.ok) return response.blob();
                throw new Error('A resposta do servidor não foi OK.');
            })
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.style.display = 'none';
                a.href = url;
                a.download = "qrcode.png";
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                a.remove();
            })
            .catch(error => {
                console.error("Erro no download:", error);
                showAlert("Erro ao tentar baixar o QR Code.", "danger");
            });
    });

    // --- FUNÇÕES AUXILIARES ---
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function showAlert(message, type) {
        alertContainer.innerHTML = `
            <div class="alert alert-${type} alert-dismissible fade show mt-3" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Fechar"></button>
            </div>`;
    }

    function hideAlert() {
        alertContainer.innerHTML = "";
    }

});
