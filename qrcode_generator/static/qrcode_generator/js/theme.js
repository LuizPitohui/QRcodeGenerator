/**
 * Sistema de Controle de Temas - Claro/Escuro
 * Gerador de QR Code - Intranet Empresarial
 */

class ThemeController {
    constructor() {
        this.currentTheme = this.getStoredTheme() || 'light';
        this.init();
    }

    init() {
        this.applyTheme(this.currentTheme);
        this.setupEventListeners();
        this.updateThemeIcon();
    }

    setupEventListeners() {
        const themeToggle = document.getElementById('themeToggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => this.toggleTheme());
        }

        // Listener para mudanças de preferência do sistema
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            if (!this.getStoredTheme()) {
                this.applyTheme(e.matches ? 'dark' : 'light');
                this.updateThemeIcon();
            }
        });
    }

    toggleTheme() {
        this.currentTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.applyTheme(this.currentTheme);
        this.storeTheme(this.currentTheme);
        this.updateThemeIcon();
        this.animateToggle();
    }

    applyTheme(theme) {
        const body = document.body;
        
        if (theme === 'dark') {
            body.setAttribute('data-theme', 'dark');
        } else {
            body.removeAttribute('data-theme');
        }

        this.currentTheme = theme;
        
        // Dispatch evento customizado para outros componentes
        window.dispatchEvent(new CustomEvent('themeChanged', { 
            detail: { theme: theme } 
        }));
    }

    updateThemeIcon() {
        const themeIcon = document.getElementById('themeIcon');
        if (themeIcon) {
            if (this.currentTheme === 'dark') {
                themeIcon.className = 'fas fa-sun';
                themeIcon.title = 'Alternar para modo claro';
            } else {
                themeIcon.className = 'fas fa-moon';
                themeIcon.title = 'Alternar para modo escuro';
            }
        }
    }

    animateToggle() {
        const themeToggle = document.getElementById('themeToggle');
        if (themeToggle) {
            themeToggle.style.transform = 'scale(0.9)';
            setTimeout(() => {
                themeToggle.style.transform = 'scale(1)';
            }, 150);
        }
    }

    storeTheme(theme) {
        try {
            localStorage.setItem('qr-generator-theme', theme);
        } catch (e) {
            console.warn('Não foi possível salvar a preferência de tema:', e);
        }
    }

    getStoredTheme() {
        try {
            return localStorage.getItem('qr-generator-theme');
        } catch (e) {
            console.warn('Não foi possível recuperar a preferência de tema:', e);
            return null;
        }
    }

    getSystemTheme() {
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }

    // Método público para obter o tema atual
    getCurrentTheme() {
        return this.currentTheme;
    }

    // Método público para definir tema programaticamente
    setTheme(theme) {
        if (theme === 'light' || theme === 'dark') {
            this.applyTheme(theme);
            this.storeTheme(theme);
            this.updateThemeIcon();
        }
    }
}

// Utilitários para animações e efeitos visuais
class UIEffects {
    static addRippleEffect(element) {
        element.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.cssText = `
                position: absolute;
                width: ${size}px;
                height: ${size}px;
                left: ${x}px;
                top: ${y}px;
                background: rgba(255, 255, 255, 0.3);
                border-radius: 50%;
                transform: scale(0);
                animation: ripple 0.6s ease-out;
                pointer-events: none;
            `;
            
            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    }

    static addHoverEffect(element) {
        element.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        element.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    }

    static addFadeInAnimation(element, delay = 0) {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            element.style.transition = 'all 0.5s ease';
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, delay);
    }
}

// Inicialização quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar controlador de tema
    window.themeController = new ThemeController();
    
    // Adicionar efeitos visuais aos botões
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        UIEffects.addRippleEffect(button);
    });
    
    // Adicionar efeito hover aos cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        UIEffects.addHoverEffect(card);
    });
    
    // Animação de fade-in para elementos principais
    const mainElements = document.querySelectorAll('.card, .stats-card');
    mainElements.forEach((element, index) => {
        UIEffects.addFadeInAnimation(element, index * 100);
    });
    
    // Listener para mudanças de tema
    window.addEventListener('themeChanged', function(e) {
        console.log('Tema alterado para:', e.detail.theme);
        
        // Aqui você pode adicionar lógica adicional quando o tema mudar
        // Por exemplo, atualizar gráficos, mapas, etc.
    });
});

// CSS para animação de ripple
const rippleCSS = `
    @keyframes ripple {
        to {
            transform: scale(2);
            opacity: 0;
        }
    }
`;

// Adicionar CSS de animação ao documento
const style = document.createElement('style');
style.textContent = rippleCSS;
document.head.appendChild(style);

// Exportar para uso global
window.ThemeController = ThemeController;
window.UIEffects = UIEffects;

