#!/bin/bash
# Script de uso rápido do Sistema Docling

echo "🎓 Sistema Docling - Uso Rápido"
echo "================================"
echo ""
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
