#!/bin/bash

# Script para inicializar repositório Git do Sistema Docling Limpo
# ================================================================

echo "🚀 Inicializando Repositório Git - Sistema Docling Limpo"
echo "========================================================"
echo ""

# Verificar se estamos no diretório correto
if [ ! -f "README.md" ]; then
    echo "❌ Execute este script no diretório Sistema_Docling_Limpo"
    exit 1
fi

echo "📁 Verificando estrutura do projeto..."
echo "✅ Estrutura encontrada:"
ls -la | head -10
echo ""

# Inicializar repositório Git
echo "🔄 Inicializando repositório Git..."
git init
echo "✅ Repositório Git inicializado!"
echo ""

# Adicionar arquivos
echo "📋 Adicionando arquivos ao Git..."
git add .
echo "✅ Arquivos adicionados!"
echo ""

# Verificar status
echo "📊 Status do repositório:"
git status
echo ""

# Fazer commit inicial
echo "💾 Fazendo commit inicial..."
git commit -m "🎉 Commit inicial - Sistema Docling Limpo

✨ Funcionalidades implementadas:
- Conversão PDF → Markdown completa
- Extração de imagens com pdfimages
- Interface web Flask (porta 9000)
- Múltiplos motores OCR (RapidOCR, EasyOCR, Tesseract)
- Sistema de download funcional
- Processamento de Markdown avançado
- Documentação completa

🚀 Sistema funcionando 100%!"
echo "✅ Commit inicial realizado!"
echo ""

# Mostrar informações do repositório
echo "📊 Informações do repositório:"
echo "============================="
echo "📁 Diretório: $(pwd)"
echo "🌿 Branch: $(git branch --show-current)"
echo "📝 Commits: $(git rev-list --count HEAD)"
echo "📅 Último commit: $(git log -1 --format=%cd --date=short)"
echo ""

# Instruções para conectar ao GitHub
echo "🔗 PRÓXIMOS PASSOS:"
echo "==================="
echo ""
echo "1. 🌐 Criar repositório no GitHub:"
echo "   - Acesse: https://github.com/new"
echo "   - Nome: sistema-docling-limpo"
echo "   - Descrição: Sistema completo para conversão de apostilas PDF em Markdown"
echo "   - Público/Privado: Sua escolha"
echo "   - NÃO inicializar com README (já temos)"
echo ""
echo "2. 🔗 Conectar repositório local ao GitHub:"
echo "   git remote add origin https://github.com/SEU_USUARIO/sistema-docling-limpo.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. 📋 Comandos úteis:"
echo "   git status                    # Ver status"
echo "   git add .                     # Adicionar mudanças"
echo "   git commit -m 'Mensagem'     # Fazer commit"
echo "   git push                      # Enviar para GitHub"
echo "   git pull                      # Baixar mudanças"
echo ""
echo "🎉 Repositório Git configurado com sucesso!"
echo "📚 Documentação disponível em README.md"
