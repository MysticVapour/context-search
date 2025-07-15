import os
import sys
from utils.file_loader import get_all_files, extract_text
from utils.embedder import TextEmbedder
from utils.store import VectorStore

def index_files(directory, chunk_size=300, overlap=50, clear_existing=False):
    """Index all supported files in a directory."""
    
    # Initialize components
    embedder = TextEmbedder()
    store = VectorStore(embedding_dim=embedder.embedding_dim)
    
    # Clear existing index if requested
    if clear_existing:
        print("Clearing existing index...")
        store.clear_index()
    
    # Get all files to index
    files = get_all_files(directory)
    print(f"Found {len(files)} files to index")
    
    if not files:
        print("No supported files found!")
        return
    
    total_chunks = 0
    
    # Process each file
    for file_path in files:
        print(f"Processing: {file_path}")
        
        # Extract text content
        content = extract_text(file_path)
        
        if not content.strip():
            print(f"  No content extracted from {file_path}")
            continue
        
        # Chunk the content
        chunks = embedder.chunk_text(content, chunk_size=chunk_size, overlap=overlap)
        print(f"  Created {len(chunks)} chunks")
        
        # Generate embeddings
        embeddings = embedder.embed_chunks(chunks)
        
        # Create metadata for each chunk
        file_chunks = []
        for i, chunk in enumerate(chunks):
            file_chunks.append({
                "file_path": file_path,
                "chunk_id": i,
                "chunk_text": chunk,
                "file_size": len(content)
            })
        
        # Add to store
        store.add_embeddings(embeddings, file_chunks)
        total_chunks += len(chunks)
        
        # Show a preview of the content
        preview = content[:200] + "..." if len(content) > 200 else content
        print(f"  Preview: {preview}")
        print()
    
    # Show final statistics
    stats = store.get_stats()
    print("=" * 50)
    print("INDEXING COMPLETE")
    print(f"Total files indexed: {stats['total_files']}")
    print(f"Total chunks: {stats['total_vectors']}")
    print(f"Embedding dimension: {stats['embedding_dimension']}")
    print("=" * 50)

if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) < 2:
        print("Usage: python index_files.py <directory> [--clear]")
        sys.exit(1)
    
    directory = sys.argv[1]
    clear_existing = "--clear" in sys.argv
    
    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist!")
        sys.exit(1)
    
    index_files(directory, clear_existing=clear_existing)
