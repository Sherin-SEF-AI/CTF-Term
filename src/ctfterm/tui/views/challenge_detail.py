"""Challenge detail view."""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Label, Static

from ...services.challenges import get_challenge_service


class ChallengeDetailView(Container):
    """Challenge detail screen."""

    DEFAULT_CSS = """
    ChallengeDetailView {
        layout: vertical;
    }
    #detail-header {
        height: 3;
        padding: 1;
    }
    #detail-description {
        height: 1fr;
        padding: 1;
    }
    #detail-buttons {
        height: 3;
        padding: 1;
    }
    """

    BINDINGS = [
        Binding("s", "submit", "Submit"),
        Binding("h", "hint", "Hint"),
        Binding("escape", "back", "Back"),
    ]

    def __init__(self, challenge_id: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.challenge_id = challenge_id

    def compose(self) -> ComposeResult:
        with Vertical():
            with Horizontal(id="detail-header"):
                yield Label("", id="challenge-title")
                yield Label("", id="challenge-category")
                yield Label("", id="challenge-points")
            yield Static("", id="detail-description")
            with Horizontal(id="detail-buttons"):
                yield Button("Submit Flag", id="submit-btn", variant="primary")
                yield Button("Show Hint", id="hint-btn")
                yield Button("Back", id="back-btn")

    def on_mount(self) -> None:
        """Load challenge on mount."""
        challenge = get_challenge_service(self.challenge_id)
        if challenge:
            self.query_one("#challenge-title", Label).update(f"[bold]{challenge['title']}[/bold]")
            self.query_one("#challenge-category", Label).update(
                f"[green]{challenge['category']}[/green]"
            )
            self.query_one("#challenge-points", Label).update(
                f"[yellow]{challenge['points']} pts[/yellow]"
            )
            self.query_one("#detail-description", Static).update(challenge["description"])

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "submit-btn":
            self.action_submit()
        elif event.button.id == "hint-btn":
            self.action_hint()
        elif event.button.id == "back-btn":
            self.action_back()

    def action_submit(self) -> None:
        """Open submit dialog."""
        self.app.notify("Submit dialog coming soon", severity="info")

    def action_hint(self) -> None:
        """Show hint."""
        challenge = get_challenge_service(self.challenge_id)
        if challenge and challenge.get("hint"):
            penalty = challenge.get("hint_penalty", 0)
            hint_text = challenge["hint"]
            if penalty > 0:
                hint_text += f"\n\n[yellow]Penalty: -{penalty} points if used[/yellow]"
            self.app.notify(hint_text, severity="info", timeout=5)
        else:
            self.app.notify("No hint available", severity="warning")

    def action_back(self) -> None:
        """Go back."""
        self.remove()

