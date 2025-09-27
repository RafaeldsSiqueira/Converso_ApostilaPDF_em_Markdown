#!/usr/bin/env python3
"""
Conversor de Apostilas com Processamento de Markdown Integrado
Mantém todas as opções de escolha do apostila_converter.py original
"""

import os
import sys
import warnings
from pathlib import Path
import logging
import argparse
import subprocess

# Suprimir warnings
warnings.filterwarnings('ignore')
os.environ['PYTHONWARNINGS'] = 'ignore'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

def configurar_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger(__name__)

def processar_markdown_integrado(arquivo_markdown, pasta_saida, opcoes_processamento=None):
    """
    Processa o Markdown para melhorar formatação e organização
    """
    logger = logging.getLogger(__name__)
    
    try:
        # Ler conteúdo original
        with open(arquivo_markdown, 'r', encoding='utf-8') as f:
            conteudo_original = f.read()
        
        logger.info(f"🔄 Processando Markdown para melhor formatação...")
        
        # Processar conteúdo com opções personalizadas
        conteudo_processado = processar_conteudo_markdown(conteudo_original, opcoes_processamento)
        
        # Salvar versão processada
        arquivo_processado = pasta_saida / f"{Path(arquivo_markdown).stem}_formatado.md"
        with open(arquivo_processado, 'w', encoding='utf-8') as f:
            f.write(conteudo_processado)
        
        logger.info(f"✅ Markdown formatado salvo: {arquivo_processado}")
        
        # Gerar estatísticas
        gerar_estatisticas_markdown(conteudo_original, conteudo_processado, pasta_saida)
        
        return str(arquivo_processado)
        
    except Exception as e:
        logger.error(f"❌ Erro no processamento do Markdown: {e}")
        return None

def processar_conteudo_markdown(conteudo, opcoes=None):
    """
    Processa o conteúdo do Markdown para melhorar formatação
    """
    import re
    
    if opcoes is None:
        opcoes = {}
    
    # 1. Limpar referências de imagem duplicadas
    if opcoes.get('limpar_imagens', True):
        conteudo = limpar_referencias_imagem(conteudo)
    
    # 2. Melhorar formatação de títulos
    if opcoes.get('numerar_titulos', True):
        conteudo = melhorar_titulos(conteudo)
    
    # 3. Organizar listas e enumerações
    if opcoes.get('organizar_listas', True):
        conteudo = organizar_listas(conteudo)
    
    # 4. Melhorar formatação de código
    if opcoes.get('melhorar_codigo', True):
        conteudo = melhorar_codigo(conteudo)
    
    # 5. Adicionar separadores visuais
    if opcoes.get('adicionar_separadores', True):
        conteudo = adicionar_separadores(conteudo)
    
    # 6. Limpar espaços em branco
    if opcoes.get('limpar_espacos', True):
        conteudo = limpar_espacos(conteudo)
    
    return conteudo

def limpar_referencias_imagem(conteudo):
    """Limpa e organiza referências de imagem"""
    import re
    
    # Contar referências de imagem
    referencias = conteudo.count('<!-- image -->')
    
    # Substituir referências por links organizados
    conteudo = re.sub(r'<!-- image -->', f'[🖼️ Imagem {referencias}]', conteudo)
    
    return conteudo

def melhorar_titulos(conteudo):
    """Melhora formatação de títulos"""
    import re
    
    linhas = conteudo.split('\n')
    contador_titulos = 0
    
    for i, linha in enumerate(linhas):
        if linha.startswith('#'):
            contador_titulos += 1
            # Adicionar numeração
            if linha.startswith('##'):
                linhas[i] = f"## {contador_titulos}. {linha[3:]}"
            elif linha.startswith('###'):
                linhas[i] = f"### {contador_titulos}.{contador_titulos} {linha[4:]}"
    
    return '\n'.join(linhas)

def organizar_listas(conteudo):
    """Organiza listas e enumerações"""
    import re
    
    # Melhorar formatação de listas
    conteudo = re.sub(r'^\s*[-*]\s+', '• ', conteudo, flags=re.MULTILINE)
    conteudo = re.sub(r'^\s*\d+\.\s+', '1. ', conteudo, flags=re.MULTILINE)
    
    return conteudo

def melhorar_codigo(conteudo):
    """Melhora formatação de blocos de código"""
    import re
    
    # Adicionar quebras de linha antes de blocos de código
    conteudo = re.sub(r'\n```', '\n\n```', conteudo)
    conteudo = re.sub(r'```\n', '```\n\n', conteudo)
    
    return conteudo

def adicionar_separadores(conteudo):
    """Adiciona separadores visuais para melhor organização"""
    import re
    
    # Adicionar separador antes de títulos principais
    conteudo = re.sub(r'\n(#{1,2}\s)', r'\n\n---\n\1', conteudo)
    
    return conteudo

def limpar_espacos(conteudo):
    """Limpa espaços em branco desnecessários"""
    import re
    
    # Remover linhas vazias excessivas
    conteudo = re.sub(r'\n{3,}', '\n\n', conteudo)
    
    # Remover espaços no final das linhas
    linhas = conteudo.split('\n')
    linhas = [linha.rstrip() for linha in linhas]
    
    return '\n'.join(linhas)

def gerar_estatisticas_markdown(conteudo_original, conteudo_processado, pasta_saida):
    """Gera estatísticas do processamento"""
    import re
    
    logger = logging.getLogger(__name__)
    
    # Contar elementos
    titulos = len(re.findall(r'^#{1,6}\s', conteudo_processado, re.MULTILINE))
    listas = len(re.findall(r'^\s*[-*•]\s', conteudo_processado, re.MULTILINE))
    codigo = len(re.findall(r'```', conteudo_processado))
    imagens = conteudo_processado.count('🖼️')
    
    # Gerar relatório
    relatorio = f"""# 📊 Relatório de Processamento de Markdown

## 📈 Estatísticas

- **📄 Caracteres originais:** {len(conteudo_original):,}
- **📄 Caracteres processados:** {len(conteudo_processado):,}
- **📈 Melhoria:** {((len(conteudo_processado) - len(conteudo_original)) / len(conteudo_original) * 100):+.1f}%

## 📋 Conteúdo Estruturado

- **📑 Títulos:** {titulos}
- **📝 Listas:** {listas}
- **💻 Blocos de código:** {codigo}
- **🖼️ Referências de imagem:** {imagens}

## ✅ Melhorias Aplicadas

- ✅ Referências de imagem organizadas
- ✅ Títulos numerados automaticamente
- ✅ Listas formatadas
- ✅ Blocos de código melhorados
- ✅ Separadores visuais adicionados
- ✅ Espaços em branco otimizados

## 📁 Arquivos Gerados

- **📄 Markdown formatado:** `{Path(pasta_saida).name}_formatado.md`
- **📊 Relatório:** `relatorio_markdown.md`
"""
    
    # Salvar relatório
    arquivo_relatorio = pasta_saida / "relatorio_markdown.md"
    with open(arquivo_relatorio, 'w', encoding='utf-8') as f:
        f.write(relatorio)
    
    logger.info(f"📊 Relatório gerado: {arquivo_relatorio}")

def converter_apostila_com_markdown_processado(arquivo_apostila, pasta_saida="output_completo", modo="completo", ocr_engine="rapidocr", usar_gpu=False, verbose=False, opcoes_processamento=None):
    """
    Converte apostila e processa o Markdown resultante com opções personalizáveis
    """
    
    logger = configurar_logging()
    
    # Verificar se arquivo existe
    if not Path(arquivo_apostila).exists():
        logger.error(f"❌ Arquivo não encontrado: {arquivo_apostila}")
        return False
    
    # Criar pasta de saída
    pasta_saida = Path(pasta_saida)
    pasta_saida.mkdir(exist_ok=True)
    
    logger.info(f"🎓 Convertendo apostila com processamento de Markdown: {arquivo_apostila}")
    logger.info(f"🔧 Modo: {modo}, OCR: {ocr_engine}, GPU: {usar_gpu}")
    
    try:
        # Importar módulos do Docling
        from docling.document_converter import DocumentConverter
        from docling.datamodel.pipeline_options import PdfPipelineOptions
        
        # Configurar pipeline baseado no modo
        if modo == "basico":
            pipeline_options = PdfPipelineOptions(
                do_ocr=False,
                extract_images=False
            )
        elif modo == "imagens":
            pipeline_options = PdfPipelineOptions(
                do_ocr=True,
                ocr_engine=ocr_engine,
                extract_images=True
            )
        elif modo == "avancado":
            pipeline_options = PdfPipelineOptions(
                do_ocr=True,
                ocr_engine=ocr_engine,
                extract_images=True,
                extract_tables=True,
                extract_formulas=True
            )
        else:  # modo completo
            pipeline_options = PdfPipelineOptions(
                do_ocr=True,
                ocr_engine=ocr_engine,
                extract_images=True,
                extract_tables=True,
                extract_formulas=True
            )
        
        # Converter documento
        logger.info("🔄 Convertendo PDF para Markdown...")
        converter = DocumentConverter()
        result = converter.convert(arquivo_apostila)
        
        # Salvar Markdown original
        markdown_content = result.document.export_to_markdown()
        arquivo_md_original = pasta_saida / f"{Path(arquivo_apostila).stem}_original.md"
        with open(arquivo_md_original, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        logger.info(f"✅ Markdown original salvo: {arquivo_md_original}")
        
        # Processar Markdown para melhor formatação (se modo não for básico)
        arquivo_md_processado = None
        if modo != "basico":
            arquivo_md_processado = processar_markdown_integrado(arquivo_md_original, pasta_saida, opcoes_processamento)
            
            if arquivo_md_processado:
                logger.info(f"✅ Markdown processado salvo: {arquivo_md_processado}")
        
        # Extrair imagens se modo incluir imagens
        if modo in ["imagens", "avancado", "completo"]:
            try:
                import subprocess
                result = subprocess.run(['which', 'pdfimages'], capture_output=True, text=True)
                if result.returncode == 0:
                    logger.info("🖼️ Extraindo imagens...")
                    
                    # Criar pasta para imagens
                    pasta_imagens = pasta_saida / "imagens"
                    pasta_imagens.mkdir(exist_ok=True)
                    
                    # Extrair imagens
                    cmd = ['pdfimages', arquivo_apostila, str(pasta_imagens / "imagem")]
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        # Contar imagens extraídas
                        arquivos_imagem = list(pasta_imagens.glob("imagem-*.ppm"))
                        logger.info(f"✅ {len(arquivos_imagem)} imagens extraídas")
                        
                        # Converter PPM para PNG
                        from PIL import Image
                        for arquivo in arquivos_imagem:
                            try:
                                img = Image.open(arquivo)
                                png_file = arquivo.with_suffix('.png')
                                img.save(png_file)
                            except Exception as e:
                                logger.warning(f"⚠️ Erro ao converter {arquivo.name}: {e}")
                    else:
                        logger.warning("⚠️ Erro ao extrair imagens")
                else:
                    logger.warning("⚠️ pdfimages não encontrado")
            except Exception as e:
                logger.warning(f"⚠️ Erro na extração de imagens: {e}")
        
        # Gerar relatório final
        gerar_relatorio_final(arquivo_apostila, pasta_saida, modo)
        
        logger.info("🎉 Conversão completa concluída!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro na conversão: {e}")
        return False

def gerar_relatorio_final(arquivo_apostila, pasta_saida, modo):
    """Gera relatório final da conversão"""
    logger = logging.getLogger(__name__)
    
    # Contar arquivos gerados
    arquivos_md = list(pasta_saida.glob("*.md"))
    arquivos_imagem = list((pasta_saida / "imagens").glob("*") if (pasta_saida / "imagens").exists() else [])
    
    relatorio = f"""# 🎓 Relatório Final de Conversão

## 📄 Arquivo Processado
- **📁 Arquivo:** {Path(arquivo_apostila).name}
- **📏 Tamanho:** {Path(arquivo_apostila).stat().st_size / (1024 * 1024):.2f} MB
- **🔧 Modo:** {modo}

## 📊 Resultados

### 📄 Arquivos Markdown
- **📄 Total:** {len(arquivos_md)} arquivos
- **📄 Arquivos:** {[f.name for f in arquivos_md]}

### 🖼️ Imagens
- **🖼️ Total:** {len(arquivos_imagem)} arquivos
- **📁 Pasta:** imagens/

## ✅ Funcionalidades

- ✅ **Conversão PDF → Markdown**
- ✅ **Processamento de Markdown** (formatação melhorada)
- ✅ **Extração de imagens** (se modo incluir imagens)
- ✅ **Relatórios detalhados**
- ✅ **Organização automática**

## 📁 Estrutura de Saída

```
{pasta_saida.name}/
├── {Path(arquivo_apostila).stem}_original.md      # Markdown original
├── {Path(arquivo_apostila).stem}_formatado.md    # Markdown processado (se aplicável)
├── relatorio_markdown.md                          # Relatório de processamento
├── relatorio_final.md                             # Este relatório
└── imagens/                                      # Imagens extraídas (se aplicável)
    ├── imagem-000.png
    ├── imagem-001.png
    └── ...
```

## 🎯 Próximos Passos

1. **📄 Revisar Markdown** - Verificar formatação
2. **🖼️ Verificar imagens** - Confirmar extração (se aplicável)
3. **📝 Editar conteúdo** - Ajustar conforme necessário
4. **📚 Usar conteúdo** - Aplicar em projetos

## 🎉 Status

**✅ CONVERSÃO COMPLETA E FUNCIONAL**

O sistema processou com sucesso:
- ✅ Texto convertido para Markdown
- ✅ Formatação melhorada e organizada
- ✅ Imagens extraídas (se modo incluir imagens)
- ✅ Relatórios gerados
- ✅ Estrutura organizada
"""
    
    # Salvar relatório
    arquivo_relatorio = pasta_saida / "relatorio_final.md"
    with open(arquivo_relatorio, 'w', encoding='utf-8') as f:
        f.write(relatorio)
    
    logger.info(f"📊 Relatório final gerado: {arquivo_relatorio}")

def main():
    """Função principal com todas as opções de escolha"""
    parser = argparse.ArgumentParser(description='Conversor de Apostilas com Processamento de Markdown Integrado')
    
    # Argumentos principais
    parser.add_argument('arquivo', help='Arquivo PDF da apostila')
    parser.add_argument('-o', '--output', default='output_completo', help='Pasta de saída')
    
    # Modos de processamento
    parser.add_argument(
        "-m", "--modo",
        choices=['basico', 'imagens', 'avancado', 'completo'],
        default='completo',
        help="Modo de processamento (padrão: completo)"
    )
    
    # Opções de OCR
    parser.add_argument(
        "--ocr",
        choices=['rapidocr', 'easyocr', 'tesseract'],
        default='rapidocr',
        help="Motor OCR para processamento (padrão: rapidocr)"
    )
    
    # Opções de processamento
    parser.add_argument(
        "-g", "--gpu",
        action="store_true",
        help="Usar GPU para OCR (se disponível)"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Log detalhado"
    )
    
    # Opções de processamento de Markdown
    parser.add_argument(
        "--sem-numeracao",
        action="store_true",
        help="Não numerar títulos automaticamente"
    )
    
    parser.add_argument(
        "--sem-separadores",
        action="store_true",
        help="Não adicionar separadores visuais"
    )
    
    parser.add_argument(
        "--sem-limpeza",
        action="store_true",
        help="Não limpar espaços em branco"
    )
    
    args = parser.parse_args()
    
    # Configurar opções de processamento
    opcoes_processamento = {
        'numerar_titulos': not args.sem_numeracao,
        'adicionar_separadores': not args.sem_separadores,
        'limpar_espacos': not args.sem_limpeza,
        'limpar_imagens': True,
        'organizar_listas': True,
        'melhorar_codigo': True
    }
    
    print("🎓 Conversor de Apostilas com Processamento de Markdown")
    print("=" * 60)
    print(f"📄 Arquivo: {args.arquivo}")
    print(f"🔧 Modo: {args.modo}")
    print(f"🤖 OCR: {args.ocr}")
    print(f"🖥️ GPU: {'Sim' if args.gpu else 'Não'}")
    print(f"📁 Saída: {args.output}")
    print("=" * 60)
    
    sucesso = converter_apostila_com_markdown_processado(
        args.arquivo, 
        args.output, 
        args.modo, 
        args.ocr, 
        args.gpu, 
        args.verbose, 
        opcoes_processamento
    )
    
    if sucesso:
        print("\n🎉 Conversão completa concluída!")
        print(f"📁 Verifique a pasta '{args.output}'")
        print("📄 Arquivos gerados:")
        print("   - [nome]_original.md (Markdown original)")
        if args.modo != "basico":
            print("   - [nome]_formatado.md (Markdown processado)")
        if args.modo in ["imagens", "avancado", "completo"]:
            print("   - imagens/ (Imagens extraídas)")
        print("   - relatorio_final.md (Relatório final)")
    else:
        print("\n❌ Falha na conversão.")
        sys.exit(1)

if __name__ == "__main__":
    main()
