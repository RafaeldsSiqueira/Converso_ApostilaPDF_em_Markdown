#!/bin/bash

# Script de diagnóstico do Sistema Conversor de Apostilas

echo "🔍 DIAGNÓSTICO DO SISTEMA - Conversor de Apostilas"
echo "=================================================="
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para verificar comando
check_command() {
    if command -v $1 &> /dev/null; then
        echo -e "${GREEN}✅${NC} $1 encontrado: $(command -v $1)"
        if [ "$1" = "python3" ] || [ "$1" = "python" ]; then
            echo "   Versão: $($1 --version 2>&1)"
        fi
        return 0
    else
        echo -e "${RED}❌${NC} $1 NÃO encontrado"
        return 1
    fi
}

# Função para verificar arquivo/diretório
check_path() {
    if [ -e "$1" ]; then
        if [ -d "$1" ]; then
            echo -e "${GREEN}✅${NC} Diretório existe: $1"
        else
            echo -e "${GREEN}✅${NC} Arquivo existe: $1"
        fi
        return 0
    else
        echo -e "${RED}❌${NC} Não encontrado: $1"
        return 1
    fi
}

# Função para verificar módulo Python
check_python_module() {
    local python_cmd=$1
    local module=$2
    
    if $python_cmd -c "import $module" 2>/dev/null; then
        echo -e "${GREEN}✅${NC} Módulo Python '$module' instalado"
        # Tentar obter versão
        version=$($python_cmd -c "import $module; print(getattr($module, '__version__', 'versão desconhecida'))" 2>/dev/null)
        if [ ! -z "$version" ] && [ "$version" != "versão desconhecida" ]; then
            echo "   Versão: $version"
        fi
        return 0
    else
        echo -e "${RED}❌${NC} Módulo Python '$module' NÃO instalado"
        return 1
    fi
}

# 1. VERIFICAR COMANDOS DO SISTEMA
echo "📋 1. VERIFICANDO COMANDOS DO SISTEMA"
echo "======================================"
check_command python3
python3_status=$?
check_command python
python_status=$?
check_command pip3
check_command pip
check_command pdfimages
pdfimages_status=$?
echo ""

# Detectar qual Python usar
if [ $python3_status -eq 0 ]; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
elif [ $python_status -eq 0 ]; then
    PYTHON_CMD="python"
    PIP_CMD="pip"
else
    PYTHON_CMD=""
fi

# 2. VERIFICAR ESTRUTURA DE DIRETÓRIOS E ARQUIVOS
echo "📁 2. VERIFICANDO ESTRUTURA DO PROJETO"
echo "======================================"
check_path "venv_docling"
venv_status=$?
check_path "venv_docling/bin/activate"
check_path "conversor_completo_markdown_opcoes.py"
check_path "backend_flask.py"
check_path "frontend.html"
check_path "requirements_frontend.txt"
check_path "instalar.sh"
check_path "iniciar_frontend.sh"
check_path "usar.sh"
echo ""

# 3. VERIFICAR PERMISSÕES DOS SCRIPTS
echo "🔐 3. VERIFICANDO PERMISSÕES DOS SCRIPTS"
echo "========================================"
for script in instalar.sh iniciar_frontend.sh usar.sh; do
    if [ -f "$script" ]; then
        if [ -x "$script" ]; then
            echo -e "${GREEN}✅${NC} $script é executável"
        else
            echo -e "${YELLOW}⚠️${NC}  $script NÃO é executável (execute: chmod +x $script)"
        fi
    fi
done
echo ""

# 4. VERIFICAR MÓDULOS PYTHON (FORA DO VENV)
if [ ! -z "$PYTHON_CMD" ]; then
    echo "🐍 4. VERIFICANDO MÓDULOS PYTHON (Sistema)"
    echo "=========================================="
    echo "Usando: $PYTHON_CMD"
    check_python_module "$PYTHON_CMD" flask
    check_python_module "$PYTHON_CMD" docling
    check_python_module "$PYTHON_CMD" PIL
    echo ""
fi

# 5. VERIFICAR AMBIENTE VIRTUAL
if [ $venv_status -eq 0 ]; then
    echo "🌐 5. VERIFICANDO AMBIENTE VIRTUAL"
    echo "=================================="
    
    # Ativar venv temporariamente em subshell
    (
        source venv_docling/bin/activate 2>/dev/null
        
        echo "Python no venv: $(which python)"
        echo "Versão: $(python --version 2>&1)"
        echo ""
        
        echo "Módulos instalados no venv:"
        check_python_module "python" flask
        check_python_module "python" flask_cors
        check_python_module "python" werkzeug
        check_python_module "python" docling
        check_python_module "python" PIL
        
        echo ""
        echo "Todos os pacotes no venv:"
        pip list 2>/dev/null | head -20
    )
else
    echo "🌐 5. VERIFICANDO AMBIENTE VIRTUAL"
    echo "=================================="
    echo -e "${RED}❌${NC} Ambiente virtual não encontrado"
    echo "   Execute: ./instalar.sh"
fi
echo ""

# 6. VERIFICAR PORTAS
echo "🌐 6. VERIFICANDO PORTAS"
echo "======================="
if command -v netstat &> /dev/null; then
    if netstat -tuln 2>/dev/null | grep -q ":9000 "; then
        echo -e "${YELLOW}⚠️${NC}  Porta 9000 já está em uso"
        echo "   Pode haver outra instância do servidor rodando"
    else
        echo -e "${GREEN}✅${NC} Porta 9000 disponível"
    fi
elif command -v ss &> /dev/null; then
    if ss -tuln 2>/dev/null | grep -q ":9000 "; then
        echo -e "${YELLOW}⚠️${NC}  Porta 9000 já está em uso"
        echo "   Pode haver outra instância do servidor rodando"
    else
        echo -e "${GREEN}✅${NC} Porta 9000 disponível"
    fi
else
    echo -e "${YELLOW}⚠️${NC}  Não foi possível verificar portas (netstat/ss não disponível)"
fi
echo ""

# 7. VERIFICAR ESPAÇO EM DISCO
echo "💾 7. VERIFICANDO ESPAÇO EM DISCO"
echo "================================"
df -h . | tail -1 | awk '{print "Disponível: " $4 " de " $2 " (" $5 " usado)"}'
echo ""

# 8. RESUMO E RECOMENDAÇÕES
echo "📊 8. RESUMO E RECOMENDAÇÕES"
echo "============================"

errors=0
warnings=0

if [ $python3_status -ne 0 ] && [ $python_status -ne 0 ]; then
    echo -e "${RED}❌ CRÍTICO:${NC} Python não encontrado"
    echo "   Solução: sudo apt install python3 python3-pip python3-venv"
    errors=$((errors + 1))
fi

if [ $pdfimages_status -ne 0 ]; then
    echo -e "${RED}❌ CRÍTICO:${NC} poppler-utils não encontrado"
    echo "   Solução: sudo apt install poppler-utils"
    errors=$((errors + 1))
fi

if [ $venv_status -ne 0 ]; then
    echo -e "${RED}❌ CRÍTICO:${NC} Ambiente virtual não encontrado"
    echo "   Solução: ./instalar.sh"
    errors=$((errors + 1))
fi

if [ ! -x "instalar.sh" ] || [ ! -x "iniciar_frontend.sh" ]; then
    echo -e "${YELLOW}⚠️  AVISO:${NC} Scripts não têm permissão de execução"
    echo "   Solução: chmod +x *.sh"
    warnings=$((warnings + 1))
fi

echo ""
if [ $errors -eq 0 ] && [ $warnings -eq 0 ]; then
    echo -e "${GREEN}✅ SISTEMA PARECE ESTAR OK!${NC}"
    echo ""
    echo "Para iniciar o frontend:"
    echo "  ./iniciar_frontend.sh"
    echo ""
    echo "Para converter via linha de comando:"
    echo "  source venv_docling/bin/activate"
    echo "  python conversor_completo_markdown_opcoes.py 'apostila.pdf' -m completo"
elif [ $errors -eq 0 ]; then
    echo -e "${YELLOW}⚠️  SISTEMA OK COM AVISOS (${warnings} aviso(s))${NC}"
    echo "   Recomenda-se corrigir os avisos acima"
else
    echo -e "${RED}❌ PROBLEMAS ENCONTRADOS (${errors} erro(s), ${warnings} aviso(s))${NC}"
    echo ""
    echo "PASSOS RECOMENDADOS:"
    echo "1. Corrigir erros críticos listados acima"
    echo "2. Executar: chmod +x *.sh"
    echo "3. Executar: ./instalar.sh"
    echo "4. Executar novamente este diagnóstico: ./diagnostico.sh"
fi

echo ""
echo "=================================================="
echo "Diagnóstico concluído em: $(date)"
echo "=================================================="

