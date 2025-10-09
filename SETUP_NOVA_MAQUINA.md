# 🖥️ Setup em Nova Máquina - Guia Completo

## 📋 Problema Comum

Ao executar `./iniciar_frontend.sh` em uma nova máquina, você pode encontrar estes erros:

```
./iniciar_frontend.sh: linha 18: venv_docling/bin/activate: Arquivo ou diretório inexistente
./iniciar_frontend.sh: linha 41: python: comando não encontrado
```

## ✅ Solução Passo a Passo

### **Passo 1: Verificar Python3**

```bash
# Verificar se Python3 está instalado
python3 --version

# Se não estiver instalado:
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
```

### **Passo 2: Dar Permissão aos Scripts**

```bash
# Tornar todos os scripts executáveis
chmod +x *.sh
```

### **Passo 3: Executar Instalação Completa**

```bash
# Executar script de instalação
./instalar.sh
```

**O que este script faz:**
- ✅ Verifica e instala Python3
- ✅ Verifica e instala pip3
- ✅ Verifica e instala poppler-utils
- ✅ Cria ambiente virtual `venv_docling`
- ✅ Instala dependências (docling, pillow, etc)
- ✅ Testa a instalação

### **Passo 4: Iniciar Frontend**

```bash
# Agora você pode iniciar o frontend
./iniciar_frontend.sh
```

**O script corrigido agora:**
- ✅ Detecta automaticamente `python3` ou `python`
- ✅ Verifica se o ambiente virtual existe
- ✅ Fornece mensagens de erro claras
- ✅ Sugere soluções quando há problemas

## 🔍 Verificações de Diagnóstico

### Verificar se ambiente virtual foi criado:
```bash
ls -la venv_docling/
```
**Deve mostrar:** `bin/`, `lib/`, `include/`, etc.

### Verificar se activate existe:
```bash
ls -la venv_docling/bin/activate
```
**Deve mostrar:** o arquivo `activate`

### Verificar Python dentro do venv:
```bash
source venv_docling/bin/activate
python --version  # Agora 'python' funciona dentro do venv
which python      # Deve mostrar: .../venv_docling/bin/python
```

### Verificar dependências instaladas:
```bash
source venv_docling/bin/activate
pip list
```
**Deve incluir:** `docling`, `Flask`, `Pillow`, etc.

## 🚨 Problemas Específicos e Soluções

### Problema 1: "venv_docling/bin/activate: Arquivo ou diretório inexistente"

**Causa:** Ambiente virtual não foi criado

**Solução:**
```bash
# Criar manualmente o ambiente virtual
python3 -m venv venv_docling

# Ativar
source venv_docling/bin/activate

# Instalar dependências
pip install docling pillow
pip install -r requirements_frontend.txt
```

### Problema 2: "python: comando não encontrado"

**Causa:** Sistema usa `python3` ao invés de `python`

**Solução 1 - Automática (scripts corrigidos):**
```bash
# Os scripts agora detectam automaticamente
./iniciar_frontend.sh
```

**Solução 2 - Criar alias permanente:**
```bash
# Instalar pacote que cria alias
sudo apt install python-is-python3

# Verificar
python --version  # Deve funcionar agora
```

**Solução 3 - Usar sempre python3:**
```bash
# Ativar venv
source venv_docling/bin/activate

# Dentro do venv, 'python' sempre funciona
python backend_flask.py
```

### Problema 3: "No module named 'flask'"

**Causa:** Dependências do frontend não foram instaladas

**Solução:**
```bash
# Ativar ambiente virtual
source venv_docling/bin/activate

# Instalar dependências do frontend
pip install -r requirements_frontend.txt

# Verificar
python -c "import flask; print('OK')"
```

### Problema 4: "No module named 'docling'"

**Causa:** Dependências principais não foram instaladas

**Solução:**
```bash
# Ativar ambiente virtual
source venv_docling/bin/activate

# Instalar docling
pip install docling pillow

# Verificar
python -c "import docling; print('OK')"
```

### Problema 5: "pdfimages não encontrado"

**Causa:** poppler-utils não está instalado

**Solução:**
```bash
sudo apt update
sudo apt install -y poppler-utils

# Verificar
pdfimages --version
```

## 🎯 Instalação Completa do Zero

Se você está começando totalmente do zero em uma nova máquina:

```bash
# 1. Atualizar sistema
sudo apt update && sudo apt upgrade -y

# 2. Instalar dependências do sistema
sudo apt install -y python3 python3-pip python3-venv poppler-utils git

# 3. Clonar repositório (se aplicável)
# git clone <seu-repositorio>
# cd Converso_ApostilaPDF_em_Markdown

# 4. Dar permissões aos scripts
chmod +x instalar.sh iniciar_frontend.sh usar.sh

# 5. Executar instalação
./instalar.sh

# 6. Iniciar frontend
./iniciar_frontend.sh

# 7. Acessar no navegador
# http://localhost:9000
```

## ✨ Fluxo de Uso Normal

Após a instalação completa, o fluxo normal é:

```bash
# Entrar no diretório
cd /caminho/para/Converso_ApostilaPDF_em_Markdown

# Iniciar frontend (já ativa o venv automaticamente)
./iniciar_frontend.sh

# Acessar interface web
# http://localhost:9000
```

**OU** para uso via linha de comando:

```bash
# Ativar ambiente
source venv_docling/bin/activate

# Converter arquivo
python conversor_completo_markdown_opcoes.py "apostila.pdf" -m completo

# Desativar ambiente quando terminar
deactivate
```

## 📊 Checklist de Instalação Bem-Sucedida

Use este checklist para garantir que tudo está funcionando:

- [ ] Python3 está instalado (`python3 --version`)
- [ ] pip3 está instalado (`pip3 --version`)
- [ ] poppler-utils está instalado (`pdfimages --version`)
- [ ] Diretório `venv_docling/` existe
- [ ] Arquivo `venv_docling/bin/activate` existe
- [ ] Scripts têm permissão de execução (`ls -la *.sh`)
- [ ] Ambiente virtual ativa sem erros (`source venv_docling/bin/activate`)
- [ ] Flask está instalado no venv (`python -c "import flask"`)
- [ ] Docling está instalado no venv (`python -c "import docling"`)
- [ ] `./iniciar_frontend.sh` executa sem erros
- [ ] Interface abre em http://localhost:9000

## 💡 Dicas Importantes

1. **Sempre use o ambiente virtual:**
   - Scripts automáticos (`./iniciar_frontend.sh`, `./usar.sh`) já ativam automaticamente
   - Para uso manual: `source venv_docling/bin/activate`

2. **Dentro do venv, use `python` (não `python3`):**
   ```bash
   source venv_docling/bin/activate
   python backend_flask.py  # ✅ Correto
   ```

3. **Fora do venv, use `python3`:**
   ```bash
   python3 conversor_completo_markdown_opcoes.py  # ✅ Correto
   ```

4. **Scripts corrigidos são inteligentes:**
   - Detectam automaticamente `python` ou `python3`
   - Verificam se venv existe antes de usar
   - Fornecem mensagens de erro claras

5. **Reinstalação limpa:**
   ```bash
   # Remover ambiente virtual antigo
   rm -rf venv_docling/
   
   # Reinstalar
   ./instalar.sh
   ```

## 🆘 Suporte Adicional

Se ainda tiver problemas:

1. **Verifique logs completos:**
   ```bash
   ./instalar.sh 2>&1 | tee instalacao.log
   ```

2. **Verifique permissões:**
   ```bash
   ls -la *.sh
   ls -la venv_docling/
   ```

3. **Verifique espaço em disco:**
   ```bash
   df -h
   ```

4. **Verifique versão do Python:**
   ```bash
   python3 --version  # Requer 3.8 ou superior
   ```

## 📚 Documentação Adicional

- **`README.md`** - Visão geral do projeto
- **`GUIA_USO_ATUALIZADO.md`** - Guia completo de uso
- **`requirements_frontend.txt`** - Dependências do frontend

---

**✅ Após seguir este guia, seu sistema deve estar 100% funcional!**

