"""Scoreboard view."""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.widgets import DataTable, Label

from ...services.scoreboard import get_scoreboard_service


class ScoreboardView(Container):
    """Scoreboard screen."""

    DEFAULT_CSS = """
    ScoreboardView {
        layout: vertical;
    }
    #scoreboard-table {
        height: 1fr;
    }
    """

    BINDINGS = [Binding("escape", "back", "Back")]

    def compose(self) -> ComposeResult:
        yield Label("[bold cyan]Leaderboard[/bold cyan]", id="scoreboard-title")
        yield DataTable(id="scoreboard-table")

    def on_mount(self) -> None:
        """Setup table on mount."""
        table = self.query_one("#scoreboard-table", DataTable)
        table.add_columns("Rank", "User", "Score", "Solves")
        self.refresh_table()

    def refresh_table(self) -> None:
        """Refresh the scoreboard."""
        table = self.query_one("#scoreboard-table", DataTable)
        scores = get_scoreboard_service()

        table.clear()
        for rank, score in enumerate(scores, 1):
            table.add_row(
                str(rank),
                score["name"],
                str(score["score"]),
                str(score["solves"]),
            )

    def action_back(self) -> None:
        """Go back."""
        self.remove()

