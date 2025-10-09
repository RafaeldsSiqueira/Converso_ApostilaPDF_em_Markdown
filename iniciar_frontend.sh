#!/bin/bash

# Script para iniciar o frontend web do Conversor de Apostilas

echo "🎓 Iniciando Frontend Web - Conversor de Apostilas"
echo "=================================================="
echo ""

# Detectar comando Python disponível
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    PIP_CMD="pip"
else
    echo "❌ Python não encontrado!"
    echo "🔄 Instale Python 3 primeiro: sudo apt install python3 python3-pip"
    exit 1
fi

echo "✅ Usando: $PYTHON_CMD"
echo ""

# Verificar se o ambiente virtual existe
if [ ! -d "venv_docling" ]; then
    echo "❌ Ambiente virtual não encontrado!"
    echo "🔄 Execute primeiro: ./instalar.sh"
    echo ""
    echo "💡 Ou crie o ambiente virtual manualmente:"
    echo "   $PYTHON_CMD -m venv venv_docling"
    echo "   source venv_docling/bin/activate"
    echo "   $PIP_CMD install -r requirements_frontend.txt"
    exit 1
fi

# Verificar se o activate existe
if [ ! -f "venv_docling/bin/activate" ]; then
    echo "❌ Arquivo de ativação do ambiente virtual não encontrado!"
    echo "🔄 O ambiente virtual pode estar corrompido. Execute: ./instalar.sh"
    exit 1
fi

# Ativar ambiente virtual
echo "🔄 Ativando ambiente virtual..."
source venv_docling/bin/activate

# Após ativar, usar python do venv (que sempre é 'python')
PYTHON_CMD="python"
PIP_CMD="pip"

# Verificar se Flask está instalado
if ! $PYTHON_CMD -c "import flask" 2>/dev/null; then
    echo "📦 Instalando dependências do frontend..."
    $PIP_CMD install -r requirements_frontend.txt
fi

# Verificar se o conversor principal existe
if [ ! -f "conversor_completo_markdown_opcoes.py" ]; then
    echo "❌ Script conversor_completo_markdown_opcoes.py não encontrado!"
    echo "🔄 Certifique-se de estar no diretório correto."
    exit 1
fi

echo "✅ Ambiente preparado!"
echo ""
echo "🌐 Iniciando servidor web..."
echo "📱 Acesse: http://localhost:9000"
echo "🛑 Para parar: Ctrl+C"
echo ""

# Iniciar servidor Flask
$PYTHON_CMD backend_flask.py
