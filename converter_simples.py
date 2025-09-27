#!/usr/bin/env python3
"""
Script simplificado para conversão de apostilas usando Docling
"""

from docling.document_converter import DocumentConverter
from pathlib import Path
import sys

def converter_apostila_simples(arquivo_entrada, pasta_saida="output"):
    """
    Converte uma apostila para Markdown de forma simples
    
    Args:
        arquivo_entrada (str): Caminho para o arquivo da apostila
        pasta_saida (str): Pasta onde salvar o resultado
    """
    
    print(f"🚀 Convertendo apostila: {arquivo_entrada}")
    
    # Verificar se o arquivo existe
    arquivo = Path(arquivo_entrada)
    if not arquivo.exists():
        print(f"❌ Arquivo não encontrado: {arquivo_entrada}")
        return False
    
    # Criar pasta de saída
    pasta_saida = Path(pasta_saida)
    pasta_saida.mkdir(exist_ok=True)
    
    try:
        # Criar conversor
        converter = DocumentConverter()
        
        # Converter documento
        print("🔄 Processando documento...")
        result = converter.convert(str(arquivo))
        
        # Salvar como Markdown
        arquivo_md = pasta_saida / f"{arquivo.stem}.md"
        markdown_content = result.document.export_to_markdown()
        
        with open(arquivo_md, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"✅ Conversão concluída!")
        print(f"📄 Markdown salvo em: {arquivo_md}")
        print(f"📊 Páginas processadas: {len(result.document.pages)}")
        print(f"📝 Tamanho do arquivo: {len(markdown_content)} caracteres")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na conversão: {e}")
        return False

def main():
    """Função principal"""
    
    if len(sys.argv) < 2:
        print("📖 Uso: python converter_simples.py <arquivo_apostila> [pasta_saida]")
        print("📖 Exemplo: python converter_simples.py minha_apostila.pdf")
        print("📖 Exemplo: python converter_simples.py minha_apostila.pdf output")
        return
    
    arquivo_entrada = sys.argv[1]
    pasta_saida = sys.argv[2] if len(sys.argv) > 2 else "output"
    
    sucesso = converter_apostila_simples(arquivo_entrada, pasta_saida)
    
    if sucesso:
        print("\n🎉 Conversão realizada com sucesso!")
        print("📁 Verifique a pasta de saída para o arquivo Markdown.")
    else:
        print("\n❌ Conversão falhou. Verifique os erros acima.")

if __name__ == "__main__":
    main()
