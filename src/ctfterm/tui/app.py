"""Main TUI application."""

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer

from .views.about import AboutView
from .views.challenge_detail import ChallengeDetailView
from .views.challenges import ChallengeListView
from .views.home import HomeView
from .views.scoreboard import ScoreboardView


class CTFTermApp(App):
    """Main CTF Terminal TUI application."""

    CSS_PATH = "styles.tcss"
    TITLE = "CTF Terminal - Capture The Flag Engine"
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("f1", "help", "Help"),
        Binding("question_mark", "help", "Help"),
        Binding("g", "scoreboard", "Scoreboard"),
        Binding("t", "toggle_theme", "Theme"),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dark_mode = True

    def compose(self) -> ComposeResult:
        yield HomeView()
        yield Footer()

    def action_quit(self) -> None:
        """Quit the application."""
        self.exit()

    def action_help(self) -> None:
        """Show help."""
        self.mount(AboutView())

    def action_scoreboard(self) -> None:
        """Show scoreboard."""
        self.mount(ScoreboardView())

    def action_toggle_theme(self) -> None:
        """Toggle dark/light theme."""
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.query("*").remove_class("light")
        else:
            self.query("*").add_class("light")


def run_app() -> None:
    """Run the TUI application."""
    app = CTFTermApp()
    app.run()

