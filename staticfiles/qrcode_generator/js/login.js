// login.js

// Adicione um log aqui para ver se o arquivo está sendo lido
console.log("Arquivo login.js carregado com sucesso.");

document.addEventListener('DOMContentLoaded', function () {
    
    // Adicione um log aqui para ver se o evento DOMContentLoaded está funcionando
    console.log("DOM totalmente carregado. O script principal vai começar.");

    const passwordInput = document.getElementById('password');
    const togglePasswordIcon = document.getElementById('togglePassword');

    // Vamos verificar se o JS encontrou os elementos HTML
    console.log("Elemento do campo de senha:", passwordInput);
    console.log("Elemento do ícone:", togglePasswordIcon);

    // Adiciona um evento de clique no ícone
    togglePasswordIcon.addEventListener('click', function () {
        
        // Log para saber se o clique foi detectado
        console.log("Ícone de senha foi clicado!");

        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        
        this.classList.toggle('fa-eye');
        this.classList.toggle('fa-eye-slash');
    });
});