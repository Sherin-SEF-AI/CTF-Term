"""Challenge list view."""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import DataTable, Input, Label, Static

from ...services.challenges import get_categories, list_challenges


class ChallengeListView(Container):
    """List of challenges with filtering."""

    DEFAULT_CSS = """
    ChallengeListView {
        layout: vertical;
    }
    #search-container {
        height: 3;
        padding: 1;
    }
    #challenges-table {
        height: 1fr;
    }
    """

    BINDINGS = [
        Binding("slash", "search", "Search"),
        Binding("c", "filter_category", "Categories"),
        Binding("enter", "view_detail", "View"),
        Binding("s", "submit", "Submit"),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_user_id = None
        self.category_filters = []

    def compose(self) -> ComposeResult:
        with Vertical():
            with Horizontal(id="search-container"):
                yield Label("Search:", id="search-label")
                yield Input(placeholder="Search challenges...", id="search-input")
            yield DataTable(id="challenges-table")

    def on_mount(self) -> None:
        """Setup table on mount."""
        table = self.query_one("#challenges-table", DataTable)
        table.add_columns("ID", "Title", "Category", "Points", "Solved")
        self.refresh_table()

    def refresh_table(self) -> None:
        """Refresh the challenges table."""
        table = self.query_one("#challenges-table", DataTable)
        search_input = self.query_one("#search-input", Input)
        search = search_input.value if search_input.value else None

        challenges = list_challenges(
            category_filters=self.category_filters if self.category_filters else None,
            search=search,
            user_id=self.current_user_id,
        )

        table.clear()
        for challenge in challenges:
            solved = "✓" if challenge.get("solved") else ""
            table.add_row(
                challenge["id"],
                challenge["title"],
                challenge["category"],
                str(challenge["points"]),
                solved,
            )

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle search input changes."""
        if event.input.id == "search-input":
            self.refresh_table()

    def action_search(self) -> None:
        """Focus search input."""
        self.query_one("#search-input", Input).focus()

    def action_filter_category(self) -> None:
        """Show category filter."""
        categories = get_categories()
        self.app.notify("Category filter coming soon", severity="info")

    def action_view_detail(self) -> None:
        """View selected challenge."""
        table = self.query_one("#challenges-table", DataTable)
        if table.cursor_row >= 0:
            row_key = table.ordered_rows[table.cursor_row]
            challenge_id = table.get_cell(row_key, "ID")
            from .challenge_detail import ChallengeDetailView
            self.app.mount(ChallengeDetailView(challenge_id))

    def action_submit(self) -> None:
        """Submit flag for selected challenge."""
        table = self.query_one("#challenges-table", DataTable)
        if table.cursor_row >= 0:
            row_key = table.ordered_rows[table.cursor_row]
            challenge_id = table.get_cell(row_key, "ID")
            self.app.notify("Submit dialog coming soon", severity="info")

