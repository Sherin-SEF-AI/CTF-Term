"""Home view."""

from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Button, Label, Static

from ...model import get_all_challenges, get_scoreboard


class HomeView(Container):
    """Home screen with welcome and quick actions."""

    DEFAULT_CSS = """
    HomeView {
        align: center middle;
    }
    #home-content {
        width: 60;
        height: auto;
    }
    """

    def compose(self) -> ComposeResult:
        with Vertical(id="home-content"):
            yield Label("[bold cyan]CTF Terminal[/bold cyan]", id="home-title")
            yield Static("", id="home-stats")
            yield Button("Open Challenges", id="challenges-btn", variant="primary")
            yield Button("Open Scoreboard", id="scoreboard-btn")
            yield Button("Import Pack", id="import-btn")

    def on_mount(self) -> None:
        """Update stats on mount."""
        challenges = get_all_challenges()
        scores = get_scoreboard()
        categories = list(set(c["category"] for c in challenges))

        stats = (
            f"[bold]Total Challenges:[/bold] {len(challenges)}\n"
            f"[bold]Categories:[/bold] {len(categories)}\n"
            f"[bold]Active Users:[/bold] {len(scores)}"
        )
        self.query_one("#home-stats", Static).update(stats)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "challenges-btn":
            from .challenges import ChallengeListView
            self.app.mount(ChallengeListView())
        elif event.button.id == "scoreboard-btn":
            from .scoreboard import ScoreboardView
            self.app.mount(ScoreboardView())
        elif event.button.id == "import-btn":
            self.app.notify("Import functionality coming soon", severity="info")

