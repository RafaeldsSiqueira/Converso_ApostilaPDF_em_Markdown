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

# Verificar e limpar ambiente virtual corrompido
if [ -d "venv_docling" ] && [ ! -f "venv_docling/bin/activate" ]; then
    echo "⚠️ Ambiente virtual corrompido detectado. Removendo..."
    rm -rf venv_docling
fi

# Remover ambiente virtual se existir
if [ -d "venv_docling" ]; then
    echo "🔄 Removendo ambiente virtual existente..."
    rm -rf venv_docling
fi

# Criar ambiente virtual
echo ""
echo "🔄 Criando ambiente virtual..."
python3 -m venv venv_docling

# Verificar se foi criado corretamente
if [ ! -f "venv_docling/bin/activate" ]; then
    echo "❌ Erro na criação do ambiente virtual!"
    echo "🔍 Verificando:"
    echo "   - Espaço em disco: $(df -h . | tail -1)"
    echo "   - Permissões: $(ls -la venv_docling/ 2>/dev/null || echo 'Diretório não existe')"
    echo "   - Python3: $(which python3)"
    exit 1
fi

echo "✅ Ambiente virtual criado com sucesso!"

# Ativar ambiente virtual
echo "🔄 Ativando ambiente virtual..."
source venv_docling/bin/activate

# Instalar dependências essenciais
echo "🔄 Instalando dependências essenciais..."
pip install -r requirements_minimal.txt

# Perguntar se quer instalar dependências completas
echo ""
echo "💡 Para instalar todas as dependências (incluindo CUDA), execute:"
echo "   pip install -r requirements.txt"
echo ""

# Verificar instalação
echo ""
echo "🧪 Testando instalação..."
if ! python -c "import docling; print('✅ Docling OK')" 2>/dev/null; then
    echo "❌ Erro: Docling não instalado corretamente"
    echo "🔄 Tentando reinstalar..."
    pip install --no-cache-dir docling
    if ! python -c "import docling; print('✅ Docling OK')" 2>/dev/null; then
        echo "❌ Falha na reinstalação do Docling"
        exit 1
    fi
fi

if ! python -c "import flask; print('✅ Flask OK')" 2>/dev/null; then
    echo "❌ Erro: Flask não instalado corretamente"
    echo "🔄 Tentando reinstalar..."
    pip install --no-cache-dir flask flask-cors werkzeug
    if ! python -c "import flask; print('✅ Flask OK')" 2>/dev/null; then
        echo "❌ Falha na reinstalação do Flask"
        exit 1
    fi
fi

echo ""
echo "🎉 Instalação concluída!"
echo "📁 Para usar o sistema:"
echo "   ./iniciar_frontend.sh"
echo ""
echo "📚 Documentação disponível:"
echo "   - README.md"
echo "   - GUIA_USO_ATUALIZADO.md"
