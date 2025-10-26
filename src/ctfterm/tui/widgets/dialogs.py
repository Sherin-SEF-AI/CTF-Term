"""Dialog widgets."""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Input, Label, Select, Static


class ConfirmDialog(Container):
    """Generic confirmation dialog."""

    DEFAULT_CSS = """
    ConfirmDialog {
        width: 50;
        height: 10;
        border: solid $primary;
        background: $surface;
    }
    """

    def __init__(self, message: str, callback=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = message
        self.callback = callback

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label(self.message, id="confirm-message")
            with Horizontal():
                yield Button("Yes", id="yes-btn", variant="success")
                yield Button("No", id="no-btn", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "yes-btn":
            if self.callback:
                self.callback(True)
        else:
            if self.callback:
                self.callback(False)
        self.remove()


class HintDialog(Container):
    """Dialog showing a hint."""

    DEFAULT_CSS = """
    HintDialog {
        width: 60;
        height: 12;
        border: solid $warning;
        background: $surface;
    }
    """

    def __init__(self, hint: str, penalty: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hint = hint
        self.penalty = penalty

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label("[bold yellow]Hint[/bold yellow]", id="hint-title")
            yield Static(self.hint, id="hint-text")
            if self.penalty > 0:
                yield Static(
                    f"[yellow]Penalty: -{self.penalty} points if used[/yellow]",
                    id="hint-penalty",
                )
            yield Button("Close", id="close-btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.remove()

    BINDINGS = [Binding("escape", "close", "Close")]

    def action_close(self) -> None:
        self.remove()


class SubmitDialog(Container):
    """Dialog for submitting a flag."""

    DEFAULT_CSS = """
    SubmitDialog {
        width: 60;
        height: 15;
        border: solid $accent;
        background: $surface;
    }
    """

    def __init__(self, callback=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.callback = callback

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label("[bold cyan]Submit Flag[/bold cyan]", id="submit-title")
            yield Label("User:", id="user-label")
            yield Input(placeholder="Enter username", id="user-input")
            yield Label("Flag:", id="flag-label")
            yield Input(placeholder="flag{...}", id="flag-input")
            with Horizontal():
                yield Button("Submit", id="submit-btn", variant="primary")
                yield Button("Cancel", id="cancel-btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel-btn":
            self.remove()
        elif event.button.id == "submit-btn":
            user_input = self.query_one("#user-input", Input)
            flag_input = self.query_one("#flag-input", Input)
            if self.callback:
                self.callback(user_input.value, flag_input.value)
            self.remove()

    BINDINGS = [Binding("escape", "close", "Close")]

    def action_close(self) -> None:
        self.remove()


class UserSelectDialog(Container):
    """Dialog for selecting or creating a user."""

    DEFAULT_CSS = """
    UserSelectDialog {
        width: 50;
        height: 15;
        border: solid $primary;
        background: $surface;
    }
    """

    def __init__(self, users: list[dict], callback=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.users = users
        self.callback = callback

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label("[bold cyan]Select User[/bold cyan]", id="user-select-title")
            yield Label("Existing users:", id="users-label")
            options = [(u["name"], u["id"]) for u in self.users]
            options.append(("+ Create New User", "new"))
            yield Select(options, id="user-select")
            yield Label("Or enter new username:", id="new-user-label")
            yield Input(placeholder="username", id="new-user-input")
            with Horizontal():
                yield Button("OK", id="ok-btn", variant="primary")
                yield Button("Cancel", id="cancel-btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel-btn":
            self.remove()
        elif event.button.id == "ok-btn":
            user_select = self.query_one("#user-select", Select)
            new_user_input = self.query_one("#new-user-input", Input)
            if self.callback:
                if user_select.value == "new":
                    self.callback(new_user_input.value)
                else:
                    self.callback(user_select.value)
            self.remove()

    BINDINGS = [Binding("escape", "close", "Close")]

    def action_close(self) -> None:
        self.remove()

