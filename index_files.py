import os 
import pymupdf as pdf
from docx import Document
from textwrap3 import wrap

def index_files(directory):
    for root, dirs, files in os.walk(directory, topdown=True):
        for file in files:
            if not is_supported(file):
                print(f"Skipping {file} because it is not a supported file type")
                continue

            file_path = os.path.join(root, file)
            file_content = ""

            if file.endswith('.pdf'):
                doc = pdf.open(file_path)
                for page in doc:
                    file_content += page.get_text()

            elif file.endswith('.docx'):
                document = Document(file_path)
                for paragraph in document.paragraphs:
                    file_content += paragraph.text

            elif file.endswith('.txt') or file.endswith('.md') or file.endswith('.py') or file.endswith('.js') or file.endswith('.json'):
                try:
                    file_content = open(file_path, 'r').read()
                except Exception as e:
                    print(f"Error reading {file}: {e}")
                    continue

            if len(file_content) > 300:
                chunks = wrap(file_content, 300)
            else:
                chunks = [file_content]
            
            

            print(file_content)

## Helper

SUPPORTED_EXTENSIONS = {'.txt', '.md', '.py', '.js', '.json', '.pdf', '.docx', '.csv'}

def is_supported(filename):
    return os.path.splitext(filename)[1].lower() in SUPPORTED_EXTENSIONS

index_files("context_search_test")
