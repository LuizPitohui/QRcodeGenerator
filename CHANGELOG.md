# Changelog - Gerador de QR Code Intranet

## Versão 2.0.0 - 02/07/2025

### ✨ Novas Funcionalidades
- **Sistema de Tema Claro/Escuro**: Implementado botão de alternância de tema com persistência no localStorage
- **CSS Externo**: Todo o CSS foi separado do HTML para melhor organização e manutenção
- **Paleta de Cores Personalizada**: Implementadas as cores especificadas para modo claro e escuro

### 🎨 Melhorias de Design
- **Correção da Navbar**: Removida sobreposição do conteúdo, adicionado padding-top adequado
- **Gradientes Atualizados**: 
  - Modo claro: Gradiente azul suave (#F2F2F2 → #E8F4FD → #D6EFFF)
  - Modo escuro: Gradiente roxo/azul mantido (#667eea → #764ba2)
- **Botão de Tema**: Adicionado botão circular no canto superior direito da navbar
- **Animações Suaves**: Transições de 0.3s para todas as mudanças de tema

### 🔧 Melhorias Técnicas
- **Arquitetura CSS**: Variáveis CSS organizadas para fácil manutenção
- **JavaScript Modular**: Sistema de controle de tema em arquivo separado
- **Responsividade Aprimorada**: Melhor adaptação em dispositivos móveis
- **Acessibilidade**: Melhor contraste e indicadores visuais

### 📱 Responsividade
- Ajustes específicos para telas menores
- Botão de tema adaptado para mobile
- Melhor espaçamento em dispositivos pequenos

### 🎯 Cores Implementadas

#### Modo Claro
- Primary: #134BF2
- Secondary: #000000
- Accent: #0C87F2
- Highlight: #1BA0F2
- Background: #F2F2F2
- Text: #000000
- Card Background: #ffffff
- Dourado: #FFD700

#### Modo Escuro
- Primary: #0F5FA6
- Secondary: #0A8CBF
- Accent: #04B2D9
- Highlight: #05DBF2
- Background: #0D0D0D
- Text: #FFFFFF
- Card Background: #1c1c1c
- Dourado: #FFD700

### 📁 Arquivos Adicionados/Modificados
- `qrcode_generator/static/qrcode_generator/css/styles.css` - CSS principal
- `qrcode_generator/static/qrcode_generator/js/theme.js` - Controle de temas
- `qrcode_generator/templates/qrcode_generator/base.html` - Template base atualizado
- `qrcode_generator/templates/qrcode_generator/index.html` - Página principal atualizada
- `qrcode_generator/templates/qrcode_generator/history.html` - Página de histórico atualizada

### 🧪 Testes Realizados
- ✅ Alternância de tema funcionando corretamente
- ✅ Persistência da preferência de tema
- ✅ Responsividade em diferentes resoluções
- ✅ Navbar não sobrepõe mais o conteúdo
- ✅ Todas as funcionalidades originais mantidas
- ✅ Compatibilidade com navegadores modernos

### 🚀 Como Usar o Novo Sistema de Temas
1. Clique no botão circular no canto superior direito da navbar
2. O tema alternará entre claro e escuro automaticamente
3. A preferência será salva e mantida nas próximas visitas
4. O ícone muda para indicar o próximo tema disponível:
   - 🌙 (lua) = clique para modo escuro
   - ☀️ (sol) = clique para modo claro

---

## Versão 1.0.0 - 02/07/2025

### 🎉 Lançamento Inicial
- Sistema completo de geração de QR Codes
- Interface responsiva e moderna
- Histórico de QR Codes gerados
- Download em formato PNG
- Suporte a múltiplos tipos de conteúdo
- Django Admin integrado

