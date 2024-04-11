"""Provides the main application class."""

##############################################################################
# Textual imports.
from textual.app import App
from textual.binding import Binding

##############################################################################
# Local imports.
from . import __version__
from .screens import Lookup


##############################################################################
class PISpy(App[None]):
    """The main application class."""

    TITLE = "PISpy"
    """The title of the application."""

    SUB_TITLE = f"The Terminal PyPi Viewer - v{__version__}"
    """The subtitle of the application."""

    BINDINGS = [Binding("ctrl+q", "quit", "Quit")]
    """The main application bindings."""

    ENABLE_COMMAND_PALETTE = False
    """Disable the command palette."""

    def on_mount(self) -> None:
        """Configure the application on startup."""
        self.push_screen(Lookup())


##############################################################################
def run() -> None:
    """Run the application."""
    PISpy().run()


### app.py ends here
