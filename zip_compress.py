import os
import shutil
from PyPDF2 import PdfFileReader
from zipfile import ZipFile, ZIP_DEFLATED

# Função para calcular o tamanho de um arquivo PDF
def get_pdf_size(file_path):
    try:
        with open(file_path, 'rb') as file:
            pdf = PdfFileReader(file)
            return file.tell()
    except Exception as e:
        print(f'Erro ao obter o tamanho do arquivo {file_path}: {e}')
        return 0

# Diretório de entrada contendo arquivos PDF
input_dir = ''

# Diretório de saída para os arquivos ZIP
output_dir = ''

# Tamanho máximo para cada arquivo ZIP (em bytes)
max_zip_size = 90 * 1024 * 1024  # 90 MB

# Inicialize variáveis
current_zip = None
current_zip_size = 0

# Percorra o diretório de entrada
for root, _, files in os.walk(input_dir):
    for filename in files:
        file_path = os.path.join(root, filename)
        file_size = os.path.getsize(file_path)

        if current_zip is None or current_zip_size + file_size > max_zip_size:
            # Fecha o arquivo ZIP atual, se houver um
            if current_zip:
                current_zip.close()

            # Cria um novo arquivo ZIP
            zip_filename = os.path.join(output_dir, f"batch_{len(os.listdir(output_dir)) + 1}.zip")
            current_zip = ZipFile(zip_filename, 'w', compression=ZIP_DEFLATED)
            current_zip_size = 0

        # Adiciona o arquivo PDF ao arquivo ZIP atual
        current_zip.write(file_path, os.path.basename(file_path))
        current_zip_size += file_size

# Fecha o último arquivo ZIP
if current_zip:
    current_zip.close()

print('Compactação concluída.')
