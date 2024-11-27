"""Provides the main application class."""

##############################################################################
# Textual imports.
from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Input

##############################################################################
# Local imports.
from .widgets import PackageInformation


##############################################################################
class PISpy(App[None]):
    """The main application class."""

    CSS = """
    Input {
        border: none;
        border-bottom: solid $foreground 20%;
        background: $panel;
        height: 2;
        &:focus {
            border: none;
            border-bottom: solid $foreground 30%;
        }
    }

    Screen:inline {
        height: 50vh;

        Input {
            display: none;
        }
    }
    """

    BINDINGS = [("escape", "quit", "Quit")]
    """The main application bindings."""

    ENABLE_COMMAND_PALETTE = False
    """Disable the command palette."""

    def __init__(self, initial_package: str | None) -> None:
        """Initialise the application.

        Args:
            initial_package: The initial package to look up.
        """
        super().__init__()
        self._package = initial_package

    def compose(self) -> ComposeResult:
        """Compose the stats screen.

        Returns:
            The stats screen's layout.
        """
        yield Input(placeholder="Name of the package to look up in PyPI")
        yield PackageInformation()

    async def on_mount(self) -> None:
        """Pre-fill the display if a package is passed on the command line."""
        if self._package is not None:
            await self.run_action(f"lookup('{self._package}')")

    @on(Input.Submitted)
    def lookup_package(self) -> None:
        """React to the user hitting enter in the input field."""
        if self.query_one(PackageInformation).show(self.query_one(Input).value):
            self.query_one(PackageInformation).focus()

    def action_lookup(self, package: str) -> None:
        """React to a hyperlink of a project being clicked on.

        Args:
            package: The name of the package to look up.
        """
        self.query_one(Input).value = package
        self.query_one(Input).cursor_position = len(package)
        self.lookup_package()


### app.py ends here
