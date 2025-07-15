import sys
import os
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.prompt import Prompt
from utils.embedder import TextEmbedder
from utils.store import VectorStore

console = Console()

def search_files(query, top_k=5, show_content=True):
    """Search for files using natural language query."""
    
    # Initialize components
    embedder = TextEmbedder()
    store = VectorStore(embedding_dim=embedder.embedding_dim)
    
    # Check if index exists
    if store.index.ntotal == 0:
        console.print("❌ No index found! Please run index_files.py first.", style="red")
        return []
    
    # Generate query embedding
    query_embedding = embedder.embed_query(query)
    
    # Search the index
    results = store.search(query_embedding, top_k=top_k)
    
    if not results:
        console.print("❌ No results found!", style="red")
        return []
    
    # Display results with rich formatting
    console.print(f"\n🔍 Search results for: [bold cyan]'{query}'[/bold cyan]")
    console.print("=" * 60)
    
    # Group results by file to avoid showing duplicate files
    file_results = {}
    for distance, metadata in results:
        file_path = metadata["file_path"]
        if file_path not in file_results:
            file_results[file_path] = []
        file_results[file_path].append((distance, metadata))
    
    # Sort files by best match
    sorted_files = sorted(file_results.items(), 
                         key=lambda x: min(result[0] for result in x[1]))
    
    for rank, (file_path, matches) in enumerate(sorted_files[:top_k], 1):
        best_match = min(matches, key=lambda x: x[0])
        distance, metadata = best_match
        
        # Create a panel for each result
        title = f"[{rank}] {os.path.basename(file_path)}"
        
        content = f"📁 [dim]{file_path}[/dim]\n"
        content += f"📊 Score: [yellow]{distance:.4f}[/yellow]\n"
        
        if show_content:
            chunk_text = metadata["chunk_text"]
            if len(chunk_text) > 200:
                chunk_text = chunk_text[:200] + "..."
            content += f"📄 [green]{chunk_text}[/green]"
        
        console.print(Panel(content, title=title, title_align="left", border_style="blue"))
    
    return results

def interactive_search():
    """Interactive search mode with rich formatting."""
    console.print(Panel.fit("🔍 Context-Aware File Search", style="bold magenta"))
    console.print("Type your search queries. Type [bold red]'quit'[/bold red] to exit.\n")
    
    while True:
        try:
            query = Prompt.ask("🔍 Search").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                console.print("👋 Goodbye!", style="bold green")
                break
            
            if not query:
                continue
            
            search_files(query)
            
        except KeyboardInterrupt:
            console.print("\n👋 Goodbye!", style="bold green")
            break
        except Exception as e:
            console.print(f"❌ Error: {e}", style="red")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # No query provided, enter interactive mode
        interactive_search()
    else:
        # Query provided as command line argument
        query = " ".join(sys.argv[1:])
        search_files(query) 