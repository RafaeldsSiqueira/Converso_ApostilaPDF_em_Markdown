#!/bin/bash

# Script para iniciar o frontend web do Conversor de Apostilas

echo "🎓 Iniciando Frontend Web - Conversor de Apostilas"
echo "=================================================="
echo ""

# Verificar se o ambiente virtual existe
if [ ! -d "venv_docling" ]; then
    echo "❌ Ambiente virtual não encontrado!"
    echo "🔄 Execute primeiro: ./instalar.sh"
    exit 1
fi

# Ativar ambiente virtual
echo "🔄 Ativando ambiente virtual..."
source venv_docling/bin/activate

# Verificar se Flask está instalado
if ! python -c "import flask" 2>/dev/null; then
    echo "📦 Instalando dependências do frontend..."
    pip install -r requirements_frontend.txt
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
python backend_flask.py
