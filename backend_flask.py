#!/usr/bin/env python3
"""
Backend Flask para o Conversor de Apostilas Docling
Interface web para facilitar o uso do sistema
"""

from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import os
import tempfile
import subprocess
import json
from pathlib import Path
import logging
from werkzeug.utils import secure_filename
import time
import threading
import uuid

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configurações
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'pdf'}

# Criar pastas necessárias
Path(UPLOAD_FOLDER).mkdir(exist_ok=True)
Path(OUTPUT_FOLDER).mkdir(exist_ok=True)

# Armazenar conversões em andamento
conversions = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def run_conversion(file_path, options, conversion_id):
    """Executa a conversão em background"""
    try:
        logger.info(f"Iniciando conversão {conversion_id} para {file_path}")
        
        # Atualizar status
        conversions[conversion_id]['status'] = 'processing'
        conversions[conversion_id]['progress'] = 10
        conversions[conversion_id]['message'] = 'Iniciando conversão...'
        
        # Preparar comando
        output_dir = Path(OUTPUT_FOLDER) / conversion_id
        output_dir.mkdir(exist_ok=True)
        
        # Construir comando
        cmd = [
            'python', 'conversor_completo_markdown_opcoes.py',
            file_path,
            '-m', options['modo'],
            '--ocr', options['ocr'],
            '-o', str(output_dir)
        ]
        
        if options.get('gpu'):
            cmd.append('-g')
        
        if not options.get('numeracao'):
            cmd.append('--sem-numeracao')
            
        if not options.get('separadores'):
            cmd.append('--sem-separadores')
        
        # Executar conversão
        conversions[conversion_id]['progress'] = 25
        conversions[conversion_id]['message'] = 'Processando PDF...'
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            conversions[conversion_id]['progress'] = 100
            conversions[conversion_id]['status'] = 'completed'
            conversions[conversion_id]['message'] = 'Conversão concluída!'
            conversions[conversion_id]['output_dir'] = str(output_dir)
            
            # Organizar arquivos em categorias
            files_by_category = {
                'markdown': [],
                'images': [],
                'reports': [],
                'others': []
            }
            
            # Listar e categorizar arquivos
            for file_path in output_dir.rglob('*'):
                if file_path.is_file():
                    file_info = {
                        'name': file_path.name,
                        'path': str(file_path),
                        'size': file_path.stat().st_size,
                        'type': 'file',
                        'relative_path': str(file_path.relative_to(output_dir))
                    }
                    
                    # Categorizar arquivos
                    if file_path.suffix == '.md':
                        if 'formatado' in file_path.name.lower():
                            files_by_category['markdown'].append({**file_info, 'category': 'formatado', 'download_name': 'apostila_formatado.md'})
                        elif file_path.name.lower() in ['relatorio_final.md', 'relatorio_markdown.md'] or file_path.name.lower().endswith('_relatorio.md'):
                            files_by_category['reports'].append({**file_info, 'download_name': 'relatorio_final.md'})
                        else:
                            files_by_category['markdown'].append({**file_info, 'category': 'original', 'download_name': 'apostila_original.md'})
                    elif file_path.suffix in ['.png', '.jpg', '.jpeg', '.ppm']:
                        files_by_category['images'].append(file_info)
                    else:
                        files_by_category['others'].append(file_info)
            
            # Adicionar diretórios
            for dir_path in output_dir.rglob('*'):
                if dir_path.is_dir() and dir_path != output_dir:
                    dir_info = {
                        'name': dir_path.name,
                        'path': str(dir_path),
                        'size': sum(f.stat().st_size for f in dir_path.rglob('*') if f.is_file()),
                        'type': 'directory',
                        'relative_path': str(dir_path.relative_to(output_dir))
                    }
                    
                    if 'imagem' in dir_path.name.lower():
                        files_by_category['images'].append(dir_info)
                    else:
                        files_by_category['others'].append(dir_info)
            
            # Garantir que sempre há uma entrada de imagens se há arquivos de imagem
            image_files = [f for f in files_by_category['images'] if f['type'] == 'file']
            image_dirs = [f for f in files_by_category['images'] if f['type'] == 'directory']
            
            if image_files and not image_dirs:
                # Se há arquivos de imagem mas não há diretório, criar entrada do diretório pai
                image_dir_path = output_dir / 'imagens'
                if image_dir_path.exists():
                    dir_info = {
                        'name': 'imagens',
                        'path': str(image_dir_path),
                        'size': sum(f.stat().st_size for f in image_dir_path.rglob('*') if f.is_file()),
                        'type': 'directory',
                        'relative_path': 'imagens'
                    }
                    files_by_category['images'].append(dir_info)
            
            conversions[conversion_id]['files'] = files_by_category
            
            logger.info(f"Conversão {conversion_id} concluída com sucesso")
        else:
            conversions[conversion_id]['status'] = 'error'
            conversions[conversion_id]['message'] = f'Erro na conversão: {result.stderr}'
            logger.error(f"Erro na conversão {conversion_id}: {result.stderr}")
            
    except Exception as e:
        conversions[conversion_id]['status'] = 'error'
        conversions[conversion_id]['message'] = f'Erro interno: {str(e)}'
        logger.error(f"Erro interno na conversão {conversion_id}: {e}")

@app.route('/')
def index():
    """Página principal - redireciona para o frontend"""
    return send_file('frontend.html')

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Endpoint para upload de arquivos"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            
            logger.info(f"Arquivo {filename} salvo em {file_path}")
            return jsonify({
                'success': True,
                'filename': filename,
                'filepath': file_path,
                'size': os.path.getsize(file_path)
            })
        else:
            return jsonify({'error': 'Tipo de arquivo não permitido'}), 400
            
    except Exception as e:
        logger.error(f"Erro no upload: {e}")
        return jsonify({'error': f'Erro no upload: {str(e)}'}), 500

@app.route('/api/convert', methods=['POST'])
def convert_file():
    """Endpoint para iniciar conversão"""
    try:
        data = request.json
        file_path = data.get('filepath')
        options = data.get('options', {})
        
        if not file_path or not os.path.exists(file_path):
            return jsonify({'error': 'Arquivo não encontrado'}), 400
        
        # Gerar ID único para a conversão
        conversion_id = str(uuid.uuid4())
        
        # Inicializar conversão
        conversions[conversion_id] = {
            'status': 'queued',
            'progress': 0,
            'message': 'Aguardando processamento...',
            'file_path': file_path,
            'options': options,
            'start_time': time.time()
        }
        
        # Iniciar conversão em thread separada
        thread = threading.Thread(
            target=run_conversion,
            args=(file_path, options, conversion_id)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'conversion_id': conversion_id,
            'message': 'Conversão iniciada'
        })
        
    except Exception as e:
        logger.error(f"Erro ao iniciar conversão: {e}")
        return jsonify({'error': f'Erro ao iniciar conversão: {str(e)}'}), 500

@app.route('/api/status/<conversion_id>')
def get_status(conversion_id):
    """Endpoint para verificar status da conversão"""
    if conversion_id not in conversions:
        return jsonify({'error': 'Conversão não encontrada'}), 404
    
    conversion = conversions[conversion_id]
    return jsonify({
        'status': conversion['status'],
        'progress': conversion['progress'],
        'message': conversion['message'],
        'files': conversion.get('files', []),
        'output_dir': conversion.get('output_dir')
    })

@app.route('/api/download/<conversion_id>/<filename>')
def download_file(conversion_id, filename):
    """Endpoint para download de arquivos"""
    try:
        if conversion_id not in conversions:
            return jsonify({'error': 'Conversão não encontrada'}), 404
        
        conversion = conversions[conversion_id]
        if conversion['status'] != 'completed':
            return jsonify({'error': 'Conversão não concluída'}), 400
        
        output_dir = conversion.get('output_dir')
        if not output_dir:
            return jsonify({'error': 'Diretório de saída não encontrado'}), 404
        
        # Mapear nomes de arquivos para nomes reais
        file_mapping = {
            'apostila_original.md': None,
            'apostila_formatado.md': None,
            'relatorio_final.md': None,
            'imagens': None
        }
        
        # Encontrar arquivos reais
        for file_path in Path(output_dir).rglob('*'):
            if file_path.is_file():
                if file_path.suffix == '.md':
                    if 'formatado' in file_path.name.lower():
                        file_mapping['apostila_formatado.md'] = str(file_path)
                    elif 'relatorio' in file_path.name.lower():
                        file_mapping['relatorio_final.md'] = str(file_path)
                    else:
                        file_mapping['apostila_original.md'] = str(file_path)
        
        # Encontrar diretório de imagens
        for dir_path in Path(output_dir).rglob('*'):
            if dir_path.is_dir() and ('imagem' in dir_path.name.lower() or dir_path.name.lower() == 'imagens'):
                file_mapping['imagens'] = str(dir_path)
                break
        
        # Verificar se o arquivo solicitado existe
        if filename not in file_mapping or file_mapping[filename] is None:
            return jsonify({'error': f'Arquivo {filename} não encontrado'}), 404
        
        file_path = file_mapping[filename]
        
        if os.path.isfile(file_path):
            # Download de arquivo individual
            return send_file(file_path, as_attachment=True, download_name=filename)
        elif os.path.isdir(file_path):
            # Download de diretório (zip)
            import zipfile
            
            zip_path = os.path.join(output_dir, f"{filename}.zip")
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(file_path):
                    for file in files:
                        file_path_full = os.path.join(root, file)
                        arcname = os.path.relpath(file_path_full, file_path)
                        zipf.write(file_path_full, arcname)
            
            return send_file(zip_path, as_attachment=True, download_name=f"{filename}.zip")
        else:
            return jsonify({'error': 'Arquivo não encontrado'}), 404
        
    except Exception as e:
        logger.error(f"Erro no download: {e}")
        return jsonify({'error': f'Erro no download: {str(e)}'}), 500

@app.route('/api/preview/<conversion_id>/<filename>')
def preview_file(conversion_id, filename):
    """Endpoint para preview de arquivos"""
    try:
        if conversion_id not in conversions:
            return jsonify({'error': 'Conversão não encontrada'}), 404
        
        conversion = conversions[conversion_id]
        if conversion['status'] != 'completed':
            return jsonify({'error': 'Conversão não concluída'}), 400
        
        output_dir = conversion.get('output_dir')
        if not output_dir:
            return jsonify({'error': 'Diretório de saída não encontrado'}), 404
        
        file_path = os.path.join(output_dir, filename)
        if not os.path.exists(file_path):
            return jsonify({'error': 'Arquivo não encontrado'}), 404
        
        # Ler conteúdo do arquivo
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return jsonify({
            'content': content,
            'filename': filename,
            'size': len(content)
        })
        
    except Exception as e:
        logger.error(f"Erro no preview: {e}")
        return jsonify({'error': f'Erro no preview: {str(e)}'}), 500

@app.route('/api/cleanup/<conversion_id>', methods=['DELETE'])
def cleanup_conversion(conversion_id):
    """Endpoint para limpeza de conversões antigas"""
    try:
        if conversion_id in conversions:
            conversion = conversions[conversion_id]
            output_dir = conversion.get('output_dir')
            
            if output_dir and os.path.exists(output_dir):
                import shutil
                shutil.rmtree(output_dir)
            
            del conversions[conversion_id]
            
            return jsonify({'success': True, 'message': 'Conversão removida'})
        else:
            return jsonify({'error': 'Conversão não encontrada'}), 404
            
    except Exception as e:
        logger.error(f"Erro na limpeza: {e}")
        return jsonify({'error': f'Erro na limpeza: {str(e)}'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint não encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Erro interno do servidor'}), 500

if __name__ == '__main__':
    print("🚀 Iniciando servidor do Conversor de Apostilas")
    print("📱 Acesse: http://localhost:8080")
    print("🛑 Para parar: Ctrl+C")
    
    # Verificar se o ambiente virtual está ativo
    try:
        import docling
        print("✅ Docling disponível")
    except ImportError:
        print("⚠️ Docling não encontrado. Ative o ambiente virtual primeiro:")
        print("   source venv_docling/bin/activate")
    
    # Porta fixa 9000
    port = 9000
    
    print(f"📱 Acesse: http://localhost:{port}")
    app.run(debug=True, host='0.0.0.0', port=port)
