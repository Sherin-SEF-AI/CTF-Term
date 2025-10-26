"""About view."""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical
from textual.widgets import Label, Static

from ... import __version__


class AboutView(Container):
    """About screen."""

    DEFAULT_CSS = """
    AboutView {
        align: center middle;
    }
    #about-content {
        width: 60;
        height: auto;
    }
    """

    BINDINGS = [Binding("escape", "back", "Back")]

    def compose(self) -> ComposeResult:
        with Vertical(id="about-content"):
            yield Label("[bold cyan]CTF Terminal[/bold cyan]", id="about-title")
            yield Static(f"Version: {__version__}", id="about-version")
            yield Static("", id="about-keys")
            yield Static("", id="about-info")

    def on_mount(self) -> None:
        """Show keyboard shortcuts."""
        keys = (
            "[bold]Keyboard Shortcuts:[/bold]\n\n"
            "F1 / ? - Help\n"
            "/ - Search\n"
            "c - Categories\n"
            "u - Users\n"
            "Enter - Open challenge\n"
            "s - Submit flag\n"
            "h - Show hint\n"
            "g - Scoreboard\n"
            "t - Toggle theme\n"
            "Esc - Back\n"
            "q - Quit"
        )
        self.query_one("#about-keys", Static).update(keys)

        info = (
            "\n[bold]Info:[/bold]\n\n"
            "Data directory: ~/.ctf/\n"
            "Database: ~/.ctf/ctf.db\n"
            "Packs: ~/.ctf/packs/"
        )
        self.query_one("#about-info", Static).update(info)

    def action_back(self) -> None:
        """Go back."""
        self.remove()

