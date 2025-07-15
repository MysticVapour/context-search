from sentence_transformers import SentenceTransformer
import numpy as np

class TextEmbedder:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """Initialize the text embedder with a sentence transformer model."""
        self.model = SentenceTransformer(model_name)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
    
    def chunk_text(self, text, chunk_size=300, overlap=50):
        """Split text into overlapping chunks."""
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            
            # Try to break at word boundaries
            if end < len(text):
                last_space = chunk.rfind(' ')
                if last_space > chunk_size * 0.7:  # Don't break too early
                    chunk = chunk[:last_space]
                    end = start + last_space
            
            chunks.append(chunk.strip())
            start = end - overlap
            
            if start >= len(text):
                break
        
        return chunks
    
    def embed_chunks(self, chunks):
        """Generate embeddings for a list of text chunks."""
        if not chunks:
            return np.array([])
        
        embeddings = self.model.encode(chunks)
        return embeddings
    
    def embed_query(self, query):
        """Generate embedding for a search query."""
        return self.model.encode([query]) 