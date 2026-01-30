import typer
from typing import Optional
from pathlib import Path
from rich.console import Console
from rich.table import Table
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from amharic_spell.core.corrector import SpellCorrector

app = typer.Typer()
console = Console()

@app.command()
def check(
    text: str = typer.Argument(..., help="Amharic text to check"),
    dictionary: Path = typer.Option("data/amharic_dictionary.txt", help="Path to dictionary"),
    model: Path = typer.Option("models/ngram_model.pkl", help="Path to trained model"),
):
    """
    Check spelling of a text string.
    """
    try:
        corrector = SpellCorrector(str(dictionary), model_path=str(model))
    except Exception as e:
        console.print(f"[bold red]Error loading resources:[/bold red] {e}")
        console.print("Did you train the model? Run [green]python scripts/train.py[/green]")
        raise typer.Exit(code=1)

    result = corrector.correct(text)
    
    console.print("\n[bold]Original:[/bold]")
    console.print(result["original_text"])
    
    console.print("\n[bold green]Corrected:[/bold green]")
    console.print(result["corrected_text"])
    
    if result["errors"]:
        console.print("\n[bold red]Errors Found:[/bold red]")
        table = Table(title="Suggestions")
        table.add_column("Word", style="red")
        table.add_column("Top Suggestion", style="green")
        table.add_column("Confidence", style="yellow")
        
        for error in result["errors"]:
            word = error["word"]
            top_sugg = error["suggestions"][0] if error["suggestions"] else ("None", 0.0)
            table.add_row(word, top_sugg[0], f"{top_sugg[1]:.4f}")
            
        console.print(table)
    else:
        console.print("\n[bold green]No errors found![/bold green]")

if __name__ == "__main__":
    app()
