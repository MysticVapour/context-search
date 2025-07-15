import faiss
import json
import os
import numpy as np
from typing import List, Dict, Tuple

class VectorStore:
    def __init__(self, embedding_dim=384, data_dir="data"):
        """Initialize the vector store with FAISS index and metadata storage."""
        self.embedding_dim = embedding_dim
        self.data_dir = data_dir
        self.index_path = os.path.join(data_dir, "index.faiss")
        self.metadata_path = os.path.join(data_dir, "metadata.json")
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize FAISS index
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.metadata = []
        
        # Load existing index and metadata if they exist
        self.load_index()
    
    def add_embeddings(self, embeddings: np.ndarray, file_chunks: List[Dict]):
        """Add embeddings and their metadata to the store."""
        if embeddings.size == 0:
            return
        
        # Add to FAISS index
        self.index.add(embeddings.astype(np.float32))
        
        # Add metadata
        self.metadata.extend(file_chunks)
        
        # Save both index and metadata
        self.save_index()
    
    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Tuple[float, Dict]]:
        """Search for similar embeddings and return results with metadata."""
        if self.index.ntotal == 0:
            return []
        
        # Search FAISS index
        distances, indices = self.index.search(query_embedding.astype(np.float32), top_k)
        
        # Get results with metadata
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            if idx < len(self.metadata):
                results.append((distance, self.metadata[idx]))
        
        return results
    
    def save_index(self):
        """Save the FAISS index and metadata to disk."""
        faiss.write_index(self.index, self.index_path)
        
        with open(self.metadata_path, 'w') as f:
            json.dump(self.metadata, f, indent=2)
    
    def load_index(self):
        """Load existing FAISS index and metadata from disk."""
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
        
        if os.path.exists(self.metadata_path):
            with open(self.metadata_path, 'r') as f:
                self.metadata = json.load(f)
    
    def clear_index(self):
        """Clear the index and metadata."""
        self.index = faiss.IndexFlatL2(self.embedding_dim)
        self.metadata = []
        
        # Remove files if they exist
        if os.path.exists(self.index_path):
            os.remove(self.index_path)
        if os.path.exists(self.metadata_path):
            os.remove(self.metadata_path)
    
    def get_stats(self):
        """Get statistics about the stored vectors."""
        return {
            "total_vectors": self.index.ntotal,
            "embedding_dimension": self.embedding_dim,
            "total_files": len(set(item["file_path"] for item in self.metadata))
        } 