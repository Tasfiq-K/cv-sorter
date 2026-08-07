from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.extractor import extract_directory

app = typer.Typer(
    help="AI-powered CV ranking system.",
    add_completion=False,
)

console = Console()


@app.command()
def extract(
    folder: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        help="Folder containing CVs.",
    )
):
    """
    Extract text from all supported documents.
    """

    console.print()

    console.print(
        Panel.fit(
            "[bold cyan]CV Extraction[/bold cyan]"
        )
    )

    documents = extract_directory(folder)

    if not documents:
        console.print("[red]No supported documents found.[/red]")
        raise typer.Exit()

    # table = Table(title="Extraction Summary")

    # table.add_column("Filename", style="cyan")
    # table.add_column("Characters", justify="right")
    # table.add_column("Preview")

    for document in documents:
        console.print(f"[bold][green]:heavy_check_mark:[/green][/bold] {document.filename}")

    console.print(
        f"\n[green]Successfully extracted {len(documents)} document(s).[/green]"
    )


def main():
    app()


if __name__ == "__main__":
    main()