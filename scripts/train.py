import sys
from pathlib import Path
import typer
from rich.console import Console
from rich.progress import track

# Add src to path so we can import the package without installation
sys.path.append(str(Path(__file__).parent.parent / "src"))

from amharic_spell.models.ngram import InterpolatedLanguageModel
from amharic_spell.preprocessing.tokenizer import AmharicTokenizer

app = typer.Typer()
console = Console()

@app.command()
def train(
    corpus_path: Path = typer.Argument(..., help="Path to the training corpus text file"),
    output_path: Path = typer.Option("models/ngram_model.pkl", help="Path to save the trained model"),
    ngram_size: int = typer.Option(3, help="Order of N-gram (default 3 for Trigram)"),
):
    """
    Train the Interpolated Amharic N-gram Model.
    """
    if not corpus_path.exists():
        console.print(f"[bold red]Error:[/bold red] Corpus file not found at {corpus_path}")
        raise typer.Exit(code=1)

    console.print(f"[bold green]Loading corpus from {corpus_path}...[/bold green]")
    
    tokenizer = AmharicTokenizer()
    tokenized_sentences = []
    
    # Read corpus line by line to avoid memory issues with huge files
    # Assuming one sentence per line or raw text. 
    # If raw text, we might want to read chunks.
    # For simplicity matching original logic, we read all but split by sentences.
    
    with open(corpus_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    console.print("[yellow]Tokenizing sentences...[/yellow]")
    raw_sentences = tokenizer.tokenize_sentence(text)
    
    for sent in track(raw_sentences, description="Tokenizing words..."):
        tokens = tokenizer.tokenize(sent)
        if tokens:
            tokenized_sentences.append(tokens)

    console.print(f"Total sentences: {len(tokenized_sentences)}")
    
    console.print("[yellow]Training Initialized Model...[/yellow]")
    model = InterpolatedLanguageModel()
    model.train(tokenized_sentences)
    
    # Create output directory if needed
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    console.print(f"[yellow]Saving model to {output_path}...[/yellow]")
    model.save(str(output_path))
    
    console.print(f"[bold green]Success![/bold green] Model saved.")

if __name__ == "__main__":
    app()
