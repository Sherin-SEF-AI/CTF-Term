"""Footer widget for key hints."""

from textual.widget import Widget


class Footer(Widget):
    """Footer showing keyboard shortcuts."""

    def render(self) -> str:
        """Render the footer."""
        return (
            "[dim]F1 Help • / Search • c Categories • u Users • s Submit • "
            "h Hint • g Scoreboard • t Theme • q Quit[/dim]"
        )

