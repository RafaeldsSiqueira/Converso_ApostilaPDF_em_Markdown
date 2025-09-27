#!/usr/bin/env python3
"""
Script principal para conversão de apostilas para Markdown usando Docling
Combina todas as funcionalidades em uma interface simples
"""

import argparse
import logging
from pathlib import Path
import sys
import json
from datetime import datetime

# Importar nossos módulos
try:
    from conversao_basica import convert_apostila_basica
    from tratamento_imagens import (
        extrair_imagens_da_apostila, 
        converter_com_imagens_inline,
        converter_com_referencias_imagens
    )
    from configuracao_avancada import (
        converter_apostila_avancada,
        comparar_motores_ocr
    )
    from processamento_lote import processar_lote
except ImportError as e:
    print(f"❌ Erro ao importar módulos: {e}")
    print("Certifique-se de que todos os scripts estão no mesmo diretório.")
    sys.exit(1)

def configurar_logging(verbose=False):
    """Configura o sistema de logging"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('docling_conversion.log')
        ]
    )

def modo_interativo():
    """Modo interativo para usuários iniciantes"""
    
    print("🎓 Conversor de Apostilas para Markdown - Modo Interativo")
    print("=" * 60)
    
    # Obter arquivo de entrada
    while True:
        caminho_arquivo = input("\n📁 Digite o caminho para sua apostila: ").strip()
        if Path(caminho_arquivo).exists():
            break
        print("❌ Arquivo não encontrado. Tente novamente.")
    
    # Escolher tipo de processamento
    print("\n🔧 Escolha o tipo de processamento:")
    print("1. Básico (rápido)")
    print("2. Com imagens extraídas")
    print("3. Avançado (máxima qualidade)")
    print("4. Comparar motores OCR")
    
    while True:
        escolha = input("\nDigite sua escolha (1-4): ").strip()
        if escolha in ['1', '2', '3', '4']:
            break
        print("❌ Escolha inválida. Digite 1, 2, 3 ou 4.")
    
    # Configurar pasta de saída
    pasta_saida = input("\n📂 Pasta de saída (Enter para 'output'): ").strip()
    if not pasta_saida:
        pasta_saida = "output"
    
    # Processar
    try:
        if escolha == '1':
            print("\n🚀 Iniciando conversão básica...")
            arquivo_md = convert_apostila_basica(caminho_arquivo, pasta_saida)
            print(f"✅ Conversão concluída! Arquivo: {arquivo_md}")
            
        elif escolha == '2':
            print("\n🚀 Iniciando conversão com imagens...")
            md_refs, imagens = converter_com_referencias_imagens(caminho_arquivo, pasta_saida)
            print(f"✅ Conversão concluída!")
            print(f"📄 Markdown: {md_refs}")
            print(f"🖼️ Imagens extraídas: {len(imagens)}")
            
        elif escolha == '3':
            print("\n🚀 Iniciando conversão avançada...")
            arquivos = converter_apostila_avancada(caminho_arquivo, pasta_saida)
            print(f"✅ Conversão concluída!")
            for formato, caminho in arquivos.items():
                print(f"📄 {formato.upper()}: {caminho}")
                
        elif escolha == '4':
            print("\n🚀 Comparando motores OCR...")
            resultados = comparar_motores_ocr(caminho_arquivo, pasta_saida)
            print("✅ Comparação concluída! Verifique as pastas de saída.")
            
    except Exception as e:
        print(f"❌ Erro durante o processamento: {e}")

def modo_comando(args):
    """Modo linha de comando para usuários avançados"""
    
    configurar_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    arquivo_entrada = Path(args.arquivo)
    if not arquivo_entrada.exists():
        logger.error(f"Arquivo não encontrado: {args.arquivo}")
        return 1
    
    pasta_saida = Path(args.output)
    pasta_saida.mkdir(exist_ok=True)
    
    try:
        if args.modo == 'basico':
            logger.info("🔄 Modo básico")
            arquivo_md = convert_apostila_basica(str(arquivo_entrada), str(pasta_saida))
            logger.info(f"✅ Arquivo gerado: {arquivo_md}")
            
        elif args.modo == 'imagens':
            logger.info("🔄 Modo com imagens")
            md_refs, imagens = converter_com_referencias_imagens(str(arquivo_entrada), str(pasta_saida))
            logger.info(f"✅ Markdown: {md_refs}")
            logger.info(f"✅ Imagens extraídas: {len(imagens)}")
            
        elif args.modo == 'avancado':
            logger.info("🔄 Modo avançado")
            arquivos = converter_apostila_avancada(str(arquivo_entrada), str(pasta_saida), args.ocr)
            logger.info("✅ Conversão avançada concluída")
            for formato, caminho in arquivos.items():
                logger.info(f"📄 {formato}: {caminho}")
                
        elif args.modo == 'lote':
            logger.info("🔄 Modo lote")
            relatorio = processar_lote(
                str(arquivo_entrada),  # pasta de entrada
                str(pasta_saida),
                args.workers,
                {'use_gpu': args.gpu}
            )
            logger.info(f"✅ Processamento em lote concluído: {relatorio['sucessos']} sucessos")
            
        elif args.modo == 'comparar':
            logger.info("🔄 Comparando motores OCR")
            resultados = comparar_motores_ocr(str(arquivo_entrada), str(pasta_saida))
            logger.info("✅ Comparação concluída")
            
        return 0
        
    except Exception as e:
        logger.error(f"❌ Erro: {e}")
        return 1

def main():
    """Função principal"""
    
    parser = argparse.ArgumentParser(
        description="Conversor de Apostilas para Markdown usando Docling",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:

  # Modo interativo (recomendado para iniciantes)
  python apostila_converter.py

  # Conversão básica
  python apostila_converter.py -m basico apostila.pdf

  # Conversão com imagens
  python apostila_converter.py -m imagens apostila.pdf

  # Conversão avançada com RapidOCR
  python apostila_converter.py -m avancado -o rapidocr apostila.pdf

  # Processamento em lote
  python apostila_converter.py -m lote pasta_com_apostilas/ -w 4

  # Comparar motores OCR
  python apostila_converter.py -m comparar apostila.pdf
        """
    )
    
    parser.add_argument(
        "arquivo", 
        nargs="?", 
        help="Arquivo ou pasta para processar"
    )
    parser.add_argument(
        "-m", "--modo",
        choices=['basico', 'imagens', 'avancado', 'lote', 'comparar'],
        default='basico',
        help="Modo de processamento"
    )
    parser.add_argument(
        "-o", "--output",
        default="output",
        help="Pasta de saída (padrão: output)"
    )
    parser.add_argument(
        "--ocr",
        choices=['rapidocr', 'easyocr', 'tesseract'],
        default='rapidocr',
        help="Motor OCR para modo avançado"
    )
    parser.add_argument(
        "-w", "--workers",
        type=int,
        default=2,
        help="Número de workers para processamento em lote"
    )
    parser.add_argument(
        "-g", "--gpu",
        action="store_true",
        help="Usar GPU para OCR"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Log detalhado"
    )
    parser.add_argument(
        "-i", "--interativo",
        action="store_true",
        help="Modo interativo"
    )
    
    args = parser.parse_args()
    
    # Modo interativo se solicitado ou se nenhum arquivo fornecido
    if args.interativo or not args.arquivo:
        modo_interativo()
        return 0
    
    # Modo linha de comando
    return modo_comando(args)

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⏹️ Processamento interrompido pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)
