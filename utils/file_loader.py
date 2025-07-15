import os
import pymupdf as pdf
from docx import Document

SUPPORTED_EXTENSIONS = {'.txt', '.md', '.py', '.js', '.json', '.pdf', '.docx', '.csv'}

def is_supported(filename):
    """Check if a file type is supported for indexing."""
    return os.path.splitext(filename)[1].lower() in SUPPORTED_EXTENSIONS

def extract_text(file_path):
    """Extract text content from a file based on its extension."""
    try:
        if file_path.endswith('.pdf'):
            doc = pdf.open(file_path)
            content = ""
            for page in doc:
                content += page.get_text()
            doc.close()
            return content

        elif file_path.endswith('.docx'):
            document = Document(file_path)
            content = ""
            for paragraph in document.paragraphs:
                content += paragraph.text + "\n"
            return content

        elif file_path.endswith(('.txt', '.md', '.py', '.js', '.json', '.csv')):
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        
        return ""
    
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

def get_all_files(directory):
    """Get all supported files from a directory recursively."""
    files = []
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            if is_supported(filename):
                files.append(os.path.join(root, filename))
    return files 