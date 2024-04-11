"""Provides the main application class."""

##############################################################################
# Textual imports.
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.widgets import Header, Footer, Input, Button

##############################################################################
# Local imports.
from . import __version__
from .widgets import PackageInfo


##############################################################################
class PISpy(App[None]):
    """The main application class."""

    CSS = """
    Header {
        HeaderIcon {
            visibility: hidden;
        }

        &.-tall {
            height: 1;
        }
    }

    Screen {
        &> Horizontal {
            height: 5;
            border: blank;
            Input {
                width: 1fr;
            }
        }
    }
    """

    TITLE = "PISpy"
    """The title of the application."""

    SUB_TITLE = f"The Terminal PyPI Viewer - v{__version__}"
    """The subtitle of the application."""

    BINDINGS = [Binding("ctrl+q", "quit", "Quit")]
    """The main application bindings."""

    ENABLE_COMMAND_PALETTE = False
    """Disable the command palette."""

    def compose(self) -> ComposeResult:
        """Compose the stats screen.

        Returns:
            The stats screen's layout.
        """
        yield Header()
        with Horizontal():
            yield Input(placeholder="Name of the package to look up in PyPI")
            yield Button("Lookup")
        yield PackageInfo()
        yield Footer()

    def on_mount(self) -> None:
        """Configure the screen once loaded up."""
        self.query_one(Input).focus()

    async def on_input_submitted(self, _: Input.Submitted) -> None:
        """React to the user hitting enter in the input field."""
        await self.query_one(PackageInfo).show(self.query_one(Input).value)

    async def action_lookup(self, package: str) -> None:
        """React to a hyperlink of a project being clicked on.

        Args:
            package: The name of the package to look up.
        """
        self.query_one(Input).value = package
        self.query_one(Input).cursor_position = len(package)
        await self.query_one(PackageInfo).show(package)

    async def on_button_pressed(self, _: Button.Pressed) -> None:
        """React to the user pressing the lookup button."""
        await self.query_one(PackageInfo).show(self.query_one(Input).value)

##############################################################################
def run() -> None:
    """Run the application."""
    PISpy().run()


### app.py ends here
