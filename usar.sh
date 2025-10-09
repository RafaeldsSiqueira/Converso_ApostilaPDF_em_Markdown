#!/bin/bash
# Script de uso rápido do Sistema Docling

echo "🎓 Sistema Docling - Uso Rápido"
echo "================================"
echo ""

# Verificar se o ambiente virtual existe
if [ ! -d "venv_docling" ]; then
    echo "❌ Ambiente virtual não encontrado!"
    echo "🔄 Execute primeiro: ./instalar.sh"
    exit 1
fi

# Verificar se o activate existe
if [ ! -f "venv_docling/bin/activate" ]; then
    echo "❌ Arquivo de ativação do ambiente virtual não encontrado!"
    echo "🔄 O ambiente virtual pode estar corrompido. Execute: ./instalar.sh"
    exit 1
fi

echo "🔄 Ativando ambiente virtual..."
source venv_docling/bin/activate
echo "✅ Ambiente ativado!"
echo ""
echo "📋 Comandos disponíveis:"
echo "1. python conversor_completo_markdown_opcoes.py 'apostila.pdf' -m completo"
echo "2. python apostila_converter.py -m imagens 'apostila.pdf'"
echo "3. python converter_simples.py"
echo "4. python teste_docling.py"
echo ""
echo "🎯 Para converter uma apostila:"
echo "python conversor_completo_markdown_opcoes.py 'sua_apostila.pdf' -m completo -o output"
echo ""
echo "💡 Nota: Dentro do ambiente virtual, use sempre 'python' (não 'python3')"
