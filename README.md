# Context-Aware Local File Search

A semantic search system that enables natural language queries over your local files using embeddings and vector search.

## 🚀 Features

- **Natural Language Search**: Search files using queries like "python script that connects to a database" or "resume with satellite project experience"
- **Multiple File Types**: Supports `.txt`, `.md`, `.py`, `.js`, `.json`, `.pdf`, `.docx`, `.csv`
- **Semantic Understanding**: Finds relevant content based on meaning, not just keywords
- **Beautiful CLI**: Rich formatting with colors, panels, and emojis
- **Interactive Mode**: Start interactive search sessions
- **Fast Vector Search**: Uses FAISS for efficient similarity search

## 📦 Installation

1. Clone the repository:

```bash
git clone <your-repo-url>
cd context-search
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## 🔧 Usage

### 1. Index Your Files

First, index the files you want to search:

```bash
python index_files.py /path/to/your/files
```

Options:

- `--clear`: Clear existing index before indexing

Example:

```bash
python index_files.py ~/Documents --clear
python index_files.py ~/Projects/my-project
```

### 2. Search Files

#### Command Line Search

```bash
python search.py "your search query"
```

Examples:

```bash
python search.py "python script that connects to a database"
python search.py "resume with satellite project experience"
python search.py "machine learning code"
```

#### Interactive Mode

```bash
python search.py
```

This starts an interactive session where you can enter multiple queries.

## 🏗️ Project Structure

```
context_search/
├── index_files.py       # Index files and build embeddings
├── search.py           # Search interface
├── utils/
│   ├── file_loader.py  # File content extraction
│   ├── embedder.py     # Text embedding and chunking
│   └── store.py        # Vector storage with FAISS
├── data/
│   ├── index.faiss     # Vector index (generated)
│   └── metadata.json   # File metadata (generated)
└── requirements.txt
```

## 📋 Example Queries

- `"python script that uses OpenAI API"`
- `"my resume with work experience"`
- `"database connection code"`
- `"project documentation about machine learning"`
- `"configuration files for deployment"`
- `"notes about satellite communications"`

## 🔧 How It Works

1. **File Crawling**: Recursively scans directories for supported file types
2. **Content Extraction**: Extracts text from various file formats
3. **Chunking**: Splits large files into 300-character chunks with 50-character overlap
4. **Embedding**: Uses `sentence-transformers` to convert text to 384-dimensional vectors
5. **Storage**: Stores vectors in FAISS index with metadata mapping
6. **Search**: Converts queries to embeddings and finds similar content

## 🎨 Features in Detail

### Smart Chunking

- Breaks large files into searchable chunks
- Preserves context with overlapping text
- Handles word boundaries intelligently

### Rich CLI Interface

- Color-coded results
- Beautiful panels and formatting
- Interactive prompts
- Emoji indicators

### Vector Search

- Uses FAISS for fast similarity search
- Supports incremental indexing
- Persistent storage

## 🛠️ Customization

### Supported File Types

Edit `utils/file_loader.py` to add more file types:

```python
SUPPORTED_EXTENSIONS = {'.txt', '.md', '.py', '.js', '.json', '.pdf', '.docx', '.csv'}
```

### Embedding Model

Change the model in `utils/embedder.py`:

```python
class TextEmbedder:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        # Try: 'all-mpnet-base-v2' for better accuracy
        # or 'paraphrase-multilingual-MiniLM-L12-v2' for multilingual support
```

### Chunk Size

Adjust chunk size in `index_files.py`:

```python
index_files(directory, chunk_size=300, overlap=50)
```

## 🔮 Future Enhancements

- [ ] GUI interface using Tkinter or Streamlit
- [ ] File type filtering in search
- [ ] Timestamp-based boosting
- [ ] Fuzzy file name matching
- [ ] RAG-style LLM integration
- [ ] Export search results
- [ ] Search history

## 🤝 Contributing

Feel free to open issues or submit pull requests to improve the system!

## 📄 License

MIT License - see LICENSE file for details.
