# 🎓 Sistema Docling - Versão Limpa e Organizada

> **Sistema completo para converter PDFs em Markdown com extração de imagens e interface web**

## 🚀 Início Rápido

### 1. **Instalação Automática**
```bash
# Instalação completa automática
./instalar.sh
```

### 2. **Uso Imediato**
```bash
# Ativar ambiente e usar
./usar.sh

# Ou converter diretamente
python3 conversor_completo_markdown_opcoes.py "apostila.pdf" -m completo
```

### 3. **Interface Web (Recomendado)**
```bash
# Iniciar interface web
./iniciar_frontend.sh

# Acessar: http://localhost:9000
# Upload → Converter → Download
```

## 📁 Estrutura do Projeto

```
Sistema_Docling_Limpo/
├── 🚀 SCRIPTS PRINCIPAIS
│   ├── conversor_completo_markdown_opcoes.py  # ⭐ PRINCIPAL - Com todas as opções
│   ├── apostila_converter.py                  # Conversor original
│   └── converter_simples.py                   # Conversor simples
├── 🌐 INTERFACE WEB
│   ├── frontend.html                          # Interface web HTML
│   ├── backend_flask.py                       # Servidor Flask (porta 9000)
│   └── requirements_frontend.txt               # Dependências Flask
├── 🔧 SCRIPTS DE INSTALAÇÃO
│   ├── instalar.sh                            # Instalação automática
│   ├── usar.sh                                # Uso rápido
│   ├── iniciar_frontend.sh                    # Iniciar interface web
│   └── inicializar_git.sh                     # Configurar Git
├── 📚 DOCUMENTAÇÃO
│   ├── README.md                              # Este arquivo
│   ├── README_ATUALIZADO.md                   # Documentação técnica
│   └── GUIA_USO_ATUALIZADO.md                # Guia completo de uso
└── 📁 OUTPUT (gerado automaticamente)
    ├── uploads/                               # Arquivos enviados
    ├── outputs/                               # Resultados das conversões
    ├── [nome]_original.md                    # Markdown original
    ├── [nome]_formatado.md                   # Markdown processado
    ├── imagens/                              # Imagens extraídas
    └── relatorio_final.md                    # Relatório final
```

## 🎯 Scripts Disponíveis

### 1. **`conversor_completo_markdown_opcoes.py`** ⭐ **PRINCIPAL**
```bash
# Uso completo com todas as opções
python3 conversor_completo_markdown_opcoes.py "apostila.pdf" -m completo

# Modos disponíveis:
python3 conversor_completo_markdown_opcoes.py "apostila.pdf" -m basico      # Apenas texto
python3 conversor_completo_markdown_opcoes.py "apostila.pdf" -m imagens     # Texto + imagens
python3 conversor_completo_markdown_opcoes.py "apostila.pdf" -m avancado    # OCR avançado
python3 conversor_completo_markdown_opcoes.py "apostila.pdf" -m completo    # Tudo (padrão)

# Opções adicionais:
python3 conversor_completo_markdown_opcoes.py "apostila.pdf" --ocr easyocr   # OCR de qualidade
python3 conversor_completo_markdown_opcoes.py "apostila.pdf" --sem-numeracao # Sem numeração
```

### 2. **`apostila_converter.py`** - Conversor Original
```bash
# Modo interativo
python3 apostila_converter.py

# Modo linha de comando
python3 apostila_converter.py -m imagens "apostila.pdf" -o output
```

### 3. **`converter_simples.py`** - Conversor Simples
```bash
# Interface amigável
python3 converter_simples.py
```

### 4. **Interface Web** 🌐 **RECOMENDADO**
```bash
# Iniciar servidor web
./iniciar_frontend.sh

# Acessar interface: http://localhost:9000
# Funcionalidades:
# - Upload de PDF via interface
# - Conversão com progresso em tempo real
# - Download de todos os arquivos gerados
# - Interface amigável e intuitiva
```

### 5. **Scripts de Instalação**
```bash
# Instalação completa
./instalar.sh

# Uso rápido
./usar.sh

# Configurar Git
./inicializar_git.sh
```

## 📊 Exemplos de Uso

### 🎓 **Conversão Completa (Recomendado)**
```bash
python3 conversor_completo_markdown_opcoes.py "apostila.pdf" -m completo -o output
```
**Resultado:**
- ✅ Markdown original + formatado
- ✅ 216 imagens extraídas
- ✅ Relatórios detalhados
- ✅ Estrutura organizada

### ⚡ **Conversão Rápida**
```bash
python3 conversor_completo_markdown_opcoes.py "apostila.pdf" -m basico
```
**Resultado:**
- ✅ Apenas Markdown (sem imagens)
- ✅ Processamento mais rápido
- ✅ Ideal para testes

### 🌐 **Interface Web (Mais Fácil)**
```bash
# Iniciar interface
./iniciar_frontend.sh

# Acessar: http://localhost:9000
# 1. Upload do PDF
# 2. Escolher opções
# 3. Converter
# 4. Download dos resultados
```
**Resultado:**
- ✅ Interface amigável
- ✅ Upload via navegador
- ✅ Progresso em tempo real
- ✅ Download organizado

## 🔧 Opções Disponíveis

### 📋 **Modos de Processamento:**
- **`-m basico`** - Apenas conversão de texto
- **`-m imagens`** - Texto + imagens extraídas
- **`-m avancado`** - Texto + imagens + OCR avançado
- **`-m completo`** - Tudo (padrão)

### 🤖 **Motores OCR:**
- **`--ocr rapidocr`** - Rápido (padrão)
- **`--ocr easyocr`** - Qualidade alta
- **`--ocr tesseract`** - Muito rápido

### ⚙️ **Opções de Processamento:**
- **`--sem-numeracao`** - Não numerar títulos
- **`--sem-separadores`** - Não adicionar separadores
- **`--sem-limpeza`** - Não limpar espaços

### 🔧 **Outras Opções:**
- **`-g, --gpu`** - Usar GPU (se disponível)
- **`-v, --verbose`** - Log detalhado
- **`-o, --output`** - Pasta de saída

## 📈 Performance

### ⏱️ **Tempos de Processamento:**
- **Modo básico:** ~2-3 minutos
- **Modo imagens:** ~8-10 minutos
- **Modo avançado:** ~15-20 minutos
- **Modo completo:** ~10-15 minutos

### 💾 **Uso de Recursos:**
- **CPU:** 2-4GB RAM
- **Disco:** ~100-200MB por apostila
- **Imagens:** +50-100MB por apostila

## 🚨 Solução de Problemas

### ❌ **Erro: "pdfimages não encontrado"**
```bash
sudo apt install poppler-utils
```

### ❌ **Erro: "No module named docling"**
```bash
source venv_docling/bin/activate
pip3 install docling
```

### ❌ **Processamento lento**
```bash
# Usar modo básico
python3 conversor_completo_markdown_opcoes.py "apostila.pdf" -m basico

# Ou limitar páginas (se implementado)
python3 conversor_completo_markdown_opcoes.py "apostila.pdf" --paginas 1-20
```

## 📋 Requisitos

- **Python:** 3.12+
- **Sistema:** Linux (Ubuntu/Debian)
- **RAM:** 4GB+ recomendado
- **Disco:** 1GB+ livre

## 🎉 Status do Projeto

**✅ SISTEMA 100% FUNCIONAL**

- ✅ Conversão de texto para Markdown
- ✅ Extração de imagens funcionando
- ✅ Interface web completa (porta 9000)
- ✅ Múltiplos modos de operação
- ✅ Scripts de instalação automática
- ✅ Scripts otimizados para CPU
- ✅ Sistema Git configurado
- ✅ Documentação completa
- ✅ Testes realizados com sucesso

## 📞 Suporte

- **Documentação:** `GUIA_USO_ATUALIZADO.md`
- **Interface Web:** `./iniciar_frontend.sh` → http://localhost:9000
- **Instalação:** `./instalar.sh`
- **Uso Rápido:** `./usar.sh`

---

**🎓 Sistema desenvolvido para conversão eficiente de apostilas PDF em Markdown com extração completa de imagens.**
# Converso_ApostilaPDF_em_Markdown
