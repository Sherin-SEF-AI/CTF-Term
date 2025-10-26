"""CLI commands."""

import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table

from . import __version__
from .db import init_db
from .model import (
    create_user,
    ensure_user,
    get_all_challenges,
    get_challenge,
    get_scoreboard,
    is_solved,
    record_solve,
)
from .packs import import_pack as _import_pack
from .paths import get_packs_dir
from .security import hash_flag, verify_flag

app = typer.Typer(name="ctf", help="CTF Terminal - Advanced Capture The Flag engine")
console = Console()


@app.command()
def version():
    """Show version and author information."""
    console.print(f"[bold cyan]ctf-term v{__version__}[/bold cyan]")
    console.print("\n[dim]Created by:[/dim] [link=https://sherinjosephroy.link]Sherin Joseph Roy[/link]")
    console.print("[dim]Co-Founder & Head of Products at[/dim] [link=https://deepmost.ai]DeepMost AI[/link]")
    console.print("\n[dim]GitHub:[/dim] [link=https://github.com/Sherin-SEF-AI]github.com/Sherin-SEF-AI[/link]")


@app.command()
def init():
    """Initialize the CTF app."""
    console.print("[bold green]Initializing CTF app...[/bold green]")
    init_db()
    console.print("✓ Database initialized")

    # Create sample pack
    packs_dir = get_packs_dir()
    sample_pack = packs_dir / "sample.yml"
    if not sample_pack.exists():
        sample_content = """pack: Sample Intro
version: 1
challenges:
  - id: rot13-hello
    title: Hello Crypto
    category: crypto
    description: |
      Caesar shift by 13. Decrypt "synt" and wrap with flag{}.
    points: 100
    hint: Think ROT13.
    hint_penalty: 20
    salt: "s1"
    flag_plain: "flag{flap}"
  - id: warmup-read
    title: Warmup Read
    category: misc
    description: |
      The flag is hidden in this description: flag{read_the_desc}
    points: 50
    hint: Look closely at the text.
    hint_penalty: 10
    salt: "s2"
    flag_plain: "flag{read_the_desc}"
"""
        sample_pack.write_text(sample_content)
        console.print(f"✓ Sample pack created at {sample_pack}")

    console.print("\n[bold]Next steps:[/bold]")
    console.print(f"  ctf import-pack {sample_pack}")
    console.print("  ctf list")


@app.command()
def import_pack(pack_path: Path):
    """Import challenges from a pack file."""
    try:
        count = _import_pack(pack_path)
        console.print(f"[bold green]✓ Imported {count} challenge(s)[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)


@app.command()
def list(category: str = None):
    """List challenges."""
    challenges = get_all_challenges()

    if category:
        challenges = [c for c in challenges if c["category"] == category]

    if not challenges:
        console.print("[yellow]No challenges found[/yellow]")
        return

    table = Table(title="Challenges")
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="magenta")
    table.add_column("Category", style="green")
    table.add_column("Points", style="yellow", justify="right")

    for challenge in challenges:
        table.add_row(
            challenge["id"],
            challenge["title"],
            challenge["category"],
            str(challenge["points"]),
        )

    console.print(table)


@app.command()
def show(challenge_id: str):
    """Show challenge details."""
    challenge = get_challenge(challenge_id)
    if not challenge:
        console.print(f"[bold red]Challenge not found: {challenge_id}[/bold red]")
        sys.exit(1)

    console.print(f"\n[bold cyan]{challenge['title']}[/bold cyan]")
    console.print(f"Category: [green]{challenge['category']}[/green]")
    console.print(f"Points: [yellow]{challenge['points']}[/yellow]")
    console.print(f"\n{challenge['description']}\n")


@app.command()
def hint(user: str, challenge_id: str):
    """Show a hint for a challenge."""
    challenge = get_challenge(challenge_id)
    if not challenge:
        console.print(f"[bold red]Challenge not found: {challenge_id}[/bold red]")
        sys.exit(1)

    if not challenge.get("hint"):
        console.print("[yellow]No hint available[/yellow]")
        return

    console.print(f"\n[bold cyan]Hint:[/bold cyan] {challenge['hint']}")
    if challenge.get("hint_penalty", 0) > 0:
        console.print(
            f"[yellow]Penalty: -{challenge['hint_penalty']} points if you use this hint[/yellow]\n"
        )


@app.command()
def submit(user: str, challenge_id: str, flag: str):
    """Submit a flag."""
    challenge = get_challenge(challenge_id)
    if not challenge:
        console.print(f"[bold red]Challenge not found: {challenge_id}[/bold red]")
        sys.exit(1)

    user_id = ensure_user(user)

    # Check if already solved
    if is_solved(user_id, challenge_id):
        console.print("[yellow]You've already solved this challenge![/yellow]")
        return

    # Verify flag
    if not verify_flag(flag, challenge["salt"], challenge["flag_hash"]):
        console.print("[bold red]Incorrect flag[/bold red]")
        sys.exit(1)

    # Ask about hint
    used_hint = False
    hint_penalty = 0
    if challenge.get("hint_penalty", 0) > 0:
        used_hint = Confirm.ask(
            "Did you view the hint?", default=False, console=console
        )
        if used_hint:
            hint_penalty = challenge.get("hint_penalty", 0)

    # Record solve
    record_solve(user_id, challenge_id, used_hint, hint_penalty)

    # Calculate points with first blood bonus
    points = challenge["points"]
    if used_hint:
        points -= hint_penalty
    
    # Check for first blood (rough check)
    from .model import get_connection
    with get_connection() as conn:
        solve_count = conn.execute(
            "SELECT COUNT(*) as count FROM solves WHERE challenge_id = ?",
            (challenge_id,)
        ).fetchone()
        first_blood = solve_count["count"] == 1
        
    if first_blood:
        bonus = int(challenge["points"] * 0.1)
        points += bonus
        console.print(f"[bold cyan]🎉 FIRST BLOOD! +{bonus} bonus points![/bold cyan]")
    
    console.print(f"[bold green]Correct! Awarded {points} pts.[/bold green]")


@app.command()
def scoreboard():
    """Show the leaderboard."""
    scores = get_scoreboard()

    if not scores:
        console.print("[yellow]No scores yet[/yellow]")
        return

    table = Table(title="Leaderboard")
    table.add_column("Rank", style="cyan", justify="right")
    table.add_column("User", style="magenta")
    table.add_column("Score", style="yellow", justify="right")
    table.add_column("Solves", style="green", justify="right")
    table.add_column("First Bloods", style="cyan", justify="right")

    for rank, score in enumerate(scores, 1):
        first_bloods = score.get("first_bloods", 0)
        table.add_row(
            str(rank),
            score["name"],
            str(score["score"]),
            str(score["solves"]),
            f"{first_bloods} 🩸" if first_bloods > 0 else "0",
        )

    console.print(table)


@app.command()
def make_flag_hash(flag: str, salt: str):
    """Generate a flag hash for pack authors."""
    flag_hash = hash_flag(salt, flag)
    console.print(f"\nFlag: {flag}")
    console.print(f"Salt: {salt}")
    console.print(f"Hash: {flag_hash}\n")


@app.command()
def tui():
    """Launch the Textual TUI."""
    from .tui.app import run_app

    run_app()


if __name__ == "__main__":
    app()

