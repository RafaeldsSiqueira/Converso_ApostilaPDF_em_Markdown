# 📦 Dependências do Sistema Conversor de Apostilas

Este documento explica os diferentes arquivos de dependências disponíveis no projeto.

## 📋 Arquivos de Requirements

### 1. `requirements_minimal.txt` ⭐ **RECOMENDADO**
- **Uso**: Instalação rápida com dependências essenciais
- **Tamanho**: ~200MB
- **Funcionalidades**: Conversão básica de PDF, servidor web
- **Instalação**: `pip install -r requirements_minimal.txt`

**Inclui**:
- Docling (conversão PDF)
- Pillow (processamento de imagens)
- Flask (servidor web)
- Dependências básicas

### 2. `requirements.txt` 📦 **COMPLETO**
- **Uso**: Todas as dependências instaladas no ambiente atual
- **Tamanho**: ~3GB
- **Funcionalidades**: Sistema completo com CUDA
- **Instalação**: `pip install -r requirements.txt`

**Inclui**:
- Todas as dependências do sistema
- Suporte CUDA para GPU
- Bibliotecas de machine learning
- Processamento avançado de imagens

### 3. `requirements_cuda.txt` 🚀 **GPU**
- **Uso**: Sistema completo com suporte CUDA
- **Tamanho**: ~3GB
- **Funcionalidades**: Aceleração por GPU NVIDIA
- **Requisitos**: NVIDIA GPU com drivers CUDA
- **Instalação**: `pip install -r requirements_cuda.txt`

**Inclui**:
- Todas as dependências essenciais
- PyTorch com CUDA
- Bibliotecas NVIDIA
- Aceleração por GPU

### 4. `requirements_frontend.txt` 🌐 **FRONTEND**
- **Uso**: Apenas dependências do servidor web
- **Tamanho**: ~10MB
- **Funcionalidades**: Interface web básica
- **Instalação**: `pip install -r requirements_frontend.txt`

**Inclui**:
- Flask
- Flask-CORS
- Werkzeug

## 🚀 Instalação Recomendada

### Para uso básico (recomendado):
```bash
./instalar.sh
```

### Para instalação manual:
```bash
# Criar ambiente virtual
python3 -m venv venv_docling
source venv_docling/bin/activate

# Instalar dependências essenciais
pip install -r requirements_minimal.txt

# Verificar instalação
python -c "import docling, flask; print('✅ Sistema OK!')"
```

### Para sistema completo com GPU:
```bash
# Após instalação básica
pip install -r requirements_cuda.txt
```

## 🔍 Verificação de Dependências

### Verificar instalação:
```bash
./diagnostico.sh
```

### Verificar módulos específicos:
```bash
source venv_docling/bin/activate
python -c "import docling; print('Docling OK')"
python -c "import flask; print('Flask OK')"
python -c "import torch; print('PyTorch OK')"
```

## 📊 Comparação de Tamanhos

| Arquivo | Tamanho | Tempo | Funcionalidades |
|---------|---------|-------|-----------------|
| `requirements_minimal.txt` | ~200MB | 2-3 min | Básico |
| `requirements_frontend.txt` | ~10MB | 30 seg | Web apenas |
| `requirements_cuda.txt` | ~3GB | 10-15 min | Completo + GPU |
| `requirements.txt` | ~3GB | 10-15 min | Completo |

## ⚠️ Notas Importantes

1. **GPU**: Para usar aceleração por GPU, é necessário:
   - NVIDIA GPU compatível
   - Drivers CUDA instalados
   - Usar `requirements_cuda.txt`

2. **Espaço em disco**: Sistema completo requer ~5GB de espaço

3. **Rede**: Primeira instalação requer conexão estável

4. **Compatibilidade**: Testado em Python 3.10+

## 🛠️ Solução de Problemas

### Erro de instalação:
```bash
# Limpar cache pip
pip cache purge

# Reinstalar
pip install --no-cache-dir -r requirements_minimal.txt
```

### Problemas com CUDA:
```bash
# Verificar GPU
nvidia-smi

# Instalar apenas CPU
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### Ambiente virtual corrompido:
```bash
# Recriar ambiente
rm -rf venv_docling
./instalar.sh
```
