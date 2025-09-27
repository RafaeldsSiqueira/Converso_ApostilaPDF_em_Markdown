#!/bin/bash
# Script de instalação automática do Sistema Docling

echo "🎓 Sistema Docling - Instalação Automática"
echo "=========================================="
echo ""

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado. Instalando..."
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv
else
    echo "✅ Python3 encontrado"
fi

# Verificar se pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 não encontrado. Instalando..."
    sudo apt install -y python3-pip
else
    echo "✅ pip3 encontrado"
fi

# Verificar se poppler-utils está instalado
if ! command -v pdfimages &> /dev/null; then
    echo "❌ poppler-utils não encontrado. Instalando..."
    sudo apt install -y poppler-utils
else
    echo "✅ poppler-utils encontrado"
fi

# Criar ambiente virtual
echo ""
echo "🔄 Criando ambiente virtual..."
python3 -m venv venv_docling

# Ativar ambiente virtual
echo "🔄 Ativando ambiente virtual..."
source venv_docling/bin/activate

# Instalar dependências
echo "🔄 Instalando dependências..."
pip install docling pillow

# Verificar instalação
echo ""
echo "🧪 Testando instalação..."
python teste_docling.py

echo ""
echo "🎉 Instalação concluída!"
echo "📁 Para usar o sistema:"
echo "   source venv_docling/bin/activate"
echo "   python conversor_completo_markdown_opcoes.py \"apostila.pdf\" -m completo"
echo ""
echo "📚 Documentação disponível:"
echo "   - README.md (este arquivo)"
echo "   - GUIA_USO_ATUALIZADO.md"
echo "   - GUIA_INSTALACAO.md"
